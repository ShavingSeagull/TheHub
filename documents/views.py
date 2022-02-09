from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
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

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def test_api_request(request):
    if 'credentials' not in request.session:
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    drive = build('drive', 'v3', credentials=credentials)

    # TODO: Tie this in with the document_list function below.
    # May need some further refining, but this appears to pull
    # through all the Docs in my Drive at work - check Sheets too
    files = drive.files().list(
        q="mimeType='application/vnd.google-apps.document' and trashed = false and sharedWithMe = true", 
        corpora="user"
        # includeItemsFromAllDrives=True,
        # supportsAllDrives=True
    ).execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    return HttpResponse(json.dumps(files))

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
    print(f"ABSOLUTE PATH OAUTH2CALLBACK: {request.build_absolute_uri(reverse('oauth2callback'))}")

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
    
    return redirect('test_api_request')

def document_list(request):
    """
    Display the main overview of documents,
    which will include Recent Docs, as well
    as ones relevant for the user. The page
    also displays the categories and tags to
    filter by, as well as a Search bar.
    """

    # TODO: Pull through the list of docs from the Drive API
    # and display them in the template, replacing the hard-coded
    # dummy examples.


    return render(request, "documents/document_list.html")
