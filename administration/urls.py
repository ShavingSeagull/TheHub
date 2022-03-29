from django.urls import path
from .views import (
    admin_area, create_user, 
    edit_user, delete_user,
    create_category, edit_category,
    delete_category,
    user_data_api
)

urlpatterns = [
    path('', admin_area, name="admin_area"),
    path('create-user', create_user, name="create_user"),
    path('edit-user', edit_user, name="edit_user"),
    path('delete_user', delete_user, name="delete_user"),
    path('create-category', create_category, name="create_category"),
    path('edit-category', edit_category, name="edit_category"),
    path('delete-category', delete_category, name="delete_category"),
    path('user-data-api/<str:username>', user_data_api, name="user_data_api"),
]
