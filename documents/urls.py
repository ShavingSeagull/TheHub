from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_overview, name="document_overview"),
    path('results', views.document_list, name="document_list"),
    path('creation-area', views.document_creation_selection, name="doc_creation_area"),
    path('create-document', views.create_document, name="create_document"),
    path('authorize', views.authorize, name="authorize"),
    path('oauth2callback', views.oauth2Callback, name="oauth2callback"),
    path('drive-api-build', views.google_drive_service_build, name="drive_api_build"),
]
