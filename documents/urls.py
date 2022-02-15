from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_overview, name="document_overview"),
    path('results', views.document_list, name="document_list"),
    path('authorize', views.authorize, name="authorize"),
    path('oauth2callback', views.oauth2Callback, name="oauth2callback"),
    path('drive_api_request', views.drive_api_request, name="drive_api_request"),
]
