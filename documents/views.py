from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import os
import os.path
import json
import google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import Category, Tag
from .helpers import *

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

@login_required
def google_drive_service_build(request):
    """
    Builds the connection to v3 of the Google Drive API
    and returns the built service object.
    """
    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])
    
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    return build('drive', 'v3', credentials=credentials)

@login_required
def drive_api_search(request, query: str, ordering: str, page_size: int):
    """
    The API call that handles file searching.
    """
    drive = google_drive_service_build(request)

    # TODO: Tie this in with the document_list function below.
    # May need some further refining, but this appears to pull
    # through all the Docs in my Drive at work - check Sheets too
    files = drive.files().list(
        q=query,
        corpora="user",
        # For production, will only need these fields:
        # nextPageToken (perhaps?),
        # files(
        # id, name, mimeType, description?, 
        # viewedByMe, viewedByMeTime, thumbnailLink?, createdTime,
        # modifiedTime, modifiedByMe, modifiedByMeTime, sharedWithMeTime)
        #
        # Will also need files(owners[0][displayName, photoLink]), but unsure of syntax
        fields="files(id, name, mimeType, description, properties, appProperties, owners)",
        orderBy=ordering,
        pageSize=page_size
        # includeItemsFromAllDrives=True,
        # supportsAllDrives=True
    ).execute()

    print(f"FILE METADATA: {files}")

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

    print(f"TAGS: {tags} / TYPE: {type(tags)}")

    file_metadata = {
        "name": f"{title}",
        "mimeType": mime_type,
        "appProperties": {
            "tags": tags,
            "category": category
        }
    }

    drive = google_drive_service_build(request)
    new_file = drive.files().create(body=file_metadata).execute()

    return new_file

@login_required
def authorize(request):
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'oauth_creds.json',
        scopes=SCOPES)

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # If your application knows which user is trying to authenticate, it can 
        # use this parameter to provide a hint to the Google Authentication Server. 
        # The server uses the hint to simplify the login flow either by prefilling the 
        # email field in the sign-in form or by selecting the appropriate multi-login session.
        login_hint=request.user.email,
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    
    return redirect(authorization_url)

def oauth2Callback(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'oauth_creds.json',
        scopes=SCOPES)
    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))

    code = request.GET.get("code")
    authorization_response = request.path
    # flow.fetch_token(authorization_response=authorization_response)
    flow.fetch_token(code=code)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}
    
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

    if 'credentials' not in request.session:
        return redirect('authorize')

    # Query needs to check for whether the document was shared with the user or whether the user owns it themselves.
    # This is due to docs that are owned directly not having a truthy shared status (as you can't share a doc with yourself).
    q=f"trashed = false and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501
    recent_docs_data = drive_api_search(request, query=q, ordering="sharedWithMeTime desc", page_size=3)
    relevant_docs_data = drive_api_search(request, query=q, ordering="viewedByMeTime desc", page_size=3)
    recent_files = json.loads(recent_docs_data)
    relevant_files = json.loads(relevant_docs_data)

    relevant_files_tags = tag_extractor(relevant_files)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "recent_files": recent_files,
        "relevant_files": relevant_files,
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
    if 'credentials' not in request.session:
        return redirect('authorize')

    results = request.GET.get('results')
    q=f"trashed = false and (sharedWithMe = true or '{request.user.email}' in owners) and (mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.google-apps.spreadsheet')" # noqa: E501

    if results == 'recent':
        docs_data = drive_api_search(request, query=q, ordering="sharedWithMeTime desc", page_size=1000)
    elif results == 'relevant':
        docs_data = drive_api_search(request, query=q, ordering="viewedByMeTime desc", page_size=1000)

    all_files = json.loads(docs_data)
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'all_files': all_files,
        'categories': categories,
        'tags': tags
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
def create_document(request):
    """
    Allows the user to create a doc from within The Hub.
    This allows for the addition of custom metadata (tags
    and a category).
    """
    doc_type = request.GET.get('doctype')
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        post_doc_type = request.POST.get('doc_type')
        doc_title = request.POST.get('doc_title')
        tag_list = request.POST.getlist('tags')
        extra_tags = request.POST.get('extra_tags')
        category = request.POST.get('categories')

        complete_tags = tag_formatter(tag_list, extra_tags)

        #TODO: Lists can't be stored as custom metadata.
        # Need to retrieve the tag list and use join(', ')
        # to convert them all into one long string.
        
        if 'credentials' not in request.session:
            return redirect('authorize')
            
        new_file = drive_api_file_upload(
            request, title=doc_title, 
            doc_type=post_doc_type, tags=complete_tags, category=category
        )

    context = {
        'doc_type_raw': doc_type,
        'doc_type': f"Google {doc_type}",
        'categories': categories,
        'tags': tags
    }

    return render(request, "documents/create_document.html", context=context)
