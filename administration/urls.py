from django.urls import path
from .views import (
    admin_area, create_user, 
    edit_user, delete_user,
    user_data_api
)

urlpatterns = [
    path('', admin_area, name="admin_area"),
    path('create-user', create_user, name="create_user"),
    path('edit-user', edit_user, name="edit_user"),
    path('delete_user', delete_user, name="delete_user"),
    path('user-data-api/<str:username>', user_data_api, name="user_data_api"),
]
