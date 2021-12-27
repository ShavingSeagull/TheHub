from django.urls import path
from .views import admin_area, create_user

urlpatterns = [
    path('', admin_area, name="admin_area"),
    path('create-user', create_user, name="create_user"),
]