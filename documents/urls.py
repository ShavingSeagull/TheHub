from django.urls import path
from .views import authorize, oauth2Callback, test_api_request

urlpatterns = [
    path('', authorize, name="tester"),
    path('oauth2callback', oauth2Callback, name="oauth2callback"),
    path('test_api_request', test_api_request, name="test_api_request"),
]
