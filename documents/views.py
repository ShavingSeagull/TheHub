from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
import os.path
import hashlib
import json
import requests
import google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from accounts.models import GoogleOauthCredentials
from .models import Category, Tag
from .helpers import *

# Global constants
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Loads the creds file URL for use with Google OAuth
# Inspiration for using the requests library to achieve this sourced from:
# https://www.codespeedy.com/how-to-download-files-from-url-using-python/
# Credit to Asma Khan
CREDS_URL = os.environ.get("OAUTH_CREDS_URL")
R = requests.get(CREDS_URL)

@login_required
def google_drive_service_build(request):
    """
    Builds the connection to v3 of the Google Drive API
    and returns the built service object.
    """
    user_creds_profile = GoogleOauthCredentials.objects.get(user=request.user)
    user_creds = user_creds_to_dict(
        user_creds_profile,
        SCOPES
    )
    credentials = google.oauth2.credentials.Credentials(
        **user_creds
    )

    # Save the credentials again in case the tokens have changed.
    # This is advised by Google.
    user_creds_profile.token = credentials.token
    user_creds_profile.refresh_token = credentials.refresh_token
    user_creds_profile.token_uri = credentials.token_uri
    user_creds_profile.client_id = credentials.client_id
    user_creds_profile.client_secret = credentials.client_secret
    user_creds_profile.save()

    return build('drive', 'v3', credentials=credentials)

@login_required
def drive_api_search(request, query: str, page_size: int, ordering: str = None):
    """
    The API call that handles file searching.
    """
    drive = google_drive_service_build(request)

    files = drive.files().list(
        q=query,
        corpora="user",
        # For production, will only need these fields:
        # nextPageToken (perhaps?),
        # files(
        # id, name, mimeType, description?, 
        # viewedByMe, viewedByMeTime, thumbnailLink?, createdTime,
        # modifiedTime, modifiedByMe, modifiedByMeTime, sharedWithMeTime)
        fields="files(id, name, mimeType, description, properties, appProperties, owners, webViewLink)",
        orderBy=ordering,
        pageSize=page_size
        # includeItemsFromAllDrives=True,
        # supportsAllDrives=True
    ).execute()

    # print(f"FILE METADATA: {files}")

    return json.dumps(files)

@login_required
def drive_api_file_upload(request, title: str, doc_type: str, tags='', category=''):
    """
    Allows a user to upload a new blank file (with title)
    to their Drive account. Includes custom metadata that
    doesn't ship with Google Docs and Sheets as standard,
    such as tags and a category.
    """
    if doc_type == 'Doc':
        mime_type = 'application/vnd.google-apps.document'
    elif doc_type == 'Sheet':
        mime_type = 'application/vnd.google-apps.spreadsheet'

    file_metadata = {
        "name": f"{title}",
        "mimeType": mime_type,
        "appProperties": {
            "tags": tags,
            "category": category
        }
    }

    drive = google_drive_service_build(request)
    created_file = drive.files().create(body=file_metadata).execute()
    new_file = drive.files().get(
        fileId=created_file.get('id'),
        fields="id, name, webViewLink, appProperties"
    ).execute()

    return new_file

@login_required
def authorize(request):
    # Retrieves the contents of the Creds file if it doesn't already exist.
    # File is stored for use by Authorize and OAuth2Callback below.
    if not os.path.exists('oauth_creds.json'):
        with open("oauth_creds.json", 'wb') as f:
            f.write(R.content)

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'oauth_creds.json',
        scopes=SCOPES)

    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))

    # Generates a random state token to prevent CSRF attacks. Not mandatory, but recommended
    # by Google.
    state_token = hashlib.sha256(os.urandom(1024)).hexdigest()

    # Generate URL for request to Google's OAuth 2.0 server.
    authorization_url, state = flow.authorization_url(
        # Enable offline access to allow the refresh of an access token without
        # re-prompting the user for permission. Recommended for web server apps by Google.
        access_type='offline',
        state=state_token,
        login_hint=request.user.email,
        # Enable incremental authorization. Recommended as a best practice by Google.
        include_granted_scopes='true')
    
    request.session['state'] = state
    
    return redirect(authorization_url)

def oauth2Callback(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    state = request.session['state']

    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'oauth_creds.json',
            scopes=SCOPES,
            state=state)
        flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))

        code = request.GET.get("code")
        authorization_response = request.path
        
        if code:
            flow.fetch_token(code=code)
        else:
            flow.fetch_token(authorization_response=authorization_response)
    except:
        # Catches any MismatchedStateErrors from Google if the user cancels the consent request.
        # State needs further work when time allows - Google's docs make using state tokens less
        # than user-friendly.
        return redirect('home')

    credentials = flow.credentials

    # Save the credentials to the DB
    user_creds = GoogleOauthCredentials.objects.get(user=request.user)
    user_creds.token = credentials.token
    user_creds.refresh_token = credentials.refresh_token
    user_creds.token_uri = credentials.token_uri
    user_creds.client_id = credentials.client_id
    user_creds.client_secret = credentials.client_secret
    user_creds.save()
    
    # Creds file is deleted for security after it has been used by the
    # callback function and the necessary data from it stored.
    if os.path.exists('oauth_creds.json'):
        os.remove('oauth_creds.json')
    
    return redirect('document_overview')

@login_required
def document_overview(request):
    """
    Display the main overview of documents,
    which will include recent docs, as well
    as ones relevant for the user. The page
    also displays the categories and tags to
    filter by, as well as a Search bar.
    """

    # TODO: Reduce to a single API request and sort the data by sharedWithMeTime and viewedByMeTime on the backend

    user_creds = GoogleOauthCredentials.objects.get(user=request.user)
    if not user_creds.token or not user_creds.refresh_token:
        return redirect('authorize')

    # Query needs to check for whether the document was shared with the user or whether the user owns it themselves.
    # This is due to docs that are owned directly not having a truthy shared status (as you can't share a doc with yourself).
    q=f"trashed = false and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501
    
    # If the user revokes access via their security settings on Google, the API call will error. This checks if the call
    # can be made and, if not, reroutes to the OAuth authorization process
    try:
        recent_docs_data = drive_api_search(request, query=q, page_size=3, ordering="sharedWithMeTime desc")
        relevant_docs_data = drive_api_search(request, query=q, page_size=3, ordering="viewedByMeTime desc")
    except:
        return redirect('authorize')
    
    recent_files = json.loads(recent_docs_data)
    relevant_files = json.loads(relevant_docs_data)

    recent_files_tags = tag_extractor(recent_files)
    relevant_files_tags = tag_extractor(relevant_files)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "recent_files": recent_files,
        "relevant_files": relevant_files,
        "recent_files_tags": recent_files_tags,
        "relevant_files_tags": relevant_files_tags,
        "categories": categories,
        "tags": tags
    }

    return render(request, "documents/document_overview.html", context=context)

@login_required
def document_list(request):
    """
    Displays the results of either the filtering options,
    the document search bar or by clicking the 'See All'
    button on the document_overview page.
    """
    user_creds = GoogleOauthCredentials.objects.get(user=request.user)
    if not user_creds.token or not user_creds.refresh_token:
        return redirect('authorize')

    results = request.GET.get('results')
    q=f"trashed = false and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501

    if results == 'recent':
        try:
            docs_data = drive_api_search(request, query=q, page_size=1000, ordering="sharedWithMeTime desc")
        except:
            return redirect('authorize')
    elif results == 'relevant':
        try:
            docs_data = drive_api_search(request, query=q, page_size=1000, ordering="viewedByMeTime desc")
        except:
            return redirect('authorize')

    all_files = json.loads(docs_data)
    file_tags = tag_extractor(all_files)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'all_files': all_files,
        'categories': categories,
        'tags': tags,
        'file_tags': file_tags
    }

    return render(request, "documents/document_list.html", context=context)

@login_required
def document_search_and_filter(request):
    """
    Handles the search bar at the top of the Document Overview page,
    as well as the filtering options on the sidebar of the
    document_base template. POST requests will be fired by the
    search bar; GET requests will be fired by the filters
    """
    user_creds = GoogleOauthCredentials.objects.get(user=request.user)
    if not user_creds.token or not user_creds.refresh_token:
        return redirect('authorize')

    categories = Category.objects.all()
    tags = Tag.objects.all()
    tag_filter = False

    if request.method == "GET":
        if request.GET.get("category"):
            frontend_search_term = Category.objects.get(name=request.GET.get('category')).friendly_name
            query = f"trashed = false and appProperties has {{key='category' and value='{request.GET.get('category')}'}} and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501
        elif request.GET.get("tag"):
            frontend_search_term = request.GET.get('tag')
            query = f"trashed = false and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501
            tag_filter = True

    elif request.method == "POST":
        search_term = request.POST.get('q')
        frontend_search_term = search_term
        query = f"trashed = false and name contains '{search_term}' and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501

    try:
        files = drive_api_search(request, query=query, page_size=1000, ordering="createdTime desc")
    except:
        return redirect('authorize')

    all_files = json.loads(files)
    file_tags = tag_extractor(all_files)
    all_tags = tag_extractor(all_files, for_frontend=False)

    # Due to Google's ridiculous rules surrounding only storing custom metadata as strings,
    # there appears to be no way to retrieve only the files that contain the tag requested
    # by the user. Therefore, all files need to be retrieved and then sorted to filter out
    # those that don't contain the requested tag.
    if tag_filter and len(all_tags) > 0:
        new_files = {'files': []}
        for file in all_files['files']:
            if 'appProperties' in file:
                if request.GET.get('tag') in file['appProperties']['tags']:
                    new_files['files'].append(file)
        all_files = new_files
    
    context = {
        'categories': categories,
        'tags': tags,
        'file_tags': file_tags,
        'all_files': all_files,
        'search_term': frontend_search_term
    }

    return render(request, "documents/document_list.html", context=context)

@login_required
def document_creation_selection(request):
    """
    Renders the view that allows users to select
    whether to create a Google Doc or a Sheet
    """
    return render(request, "documents/document_creation_selection.html")

@login_required
def document_create(request):
    """
    Allows the user to create a doc from within The Hub.
    This allows for the addition of custom metadata (tags
    and a category).
    """
    user_creds = GoogleOauthCredentials.objects.get(user=request.user)
    if not user_creds.token or not user_creds.refresh_token:
        return redirect('authorize')

    doc_type = request.GET.get('doctype') if request.GET.get('doctype') else 'Doc'
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        request_body = json.loads(request.body)
        post_doc_type = request_body['doc_type']
        doc_title = request_body['doc_title']
        tag_list = request_body['tag_list']
        extra_tags = request_body['extra_tags']
        category = request_body['categories']

        complete_tags = tag_formatter(tag_list, extra_tags)
        extra_tags_for_db = extra_tag_db_formatter(extra_tags)

        if extra_tags_for_db:
            for tag in extra_tags_for_db:
                try:
                    Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    Tag.objects.create(name=tag)
        
        try:
            new_file = drive_api_file_upload(
                request, title=doc_title, 
                doc_type=post_doc_type, tags=complete_tags, category=category
            )
        except:
            # Authorization ends up redirecting to the Document Overview page instead. This message is to prevent any confusion.
            messages.info(request, "Re-authorization was needed. Please proceed with document creation again.")
            return redirect('authorize')

        return JsonResponse(new_file, safe=False)

    context = {
        'doc_type_raw': doc_type,
        'doc_type': f"Google {doc_type}",
        'categories': categories,
        'tags': tags
    }

    return render(request, "documents/document_create.html", context=context)
