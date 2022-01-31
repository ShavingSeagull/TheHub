from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name="document_list"),
    path('authorize', views.authorize, name="tester"),
    path('oauth2callback', views.oauth2Callback, name="oauth2callback"),
    path('test_api_request', views.test_api_request, name="test_api_request"),
]
