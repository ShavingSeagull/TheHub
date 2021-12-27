from django.urls import path
from .views import view_profile

urlpatterns = [
    path('', view_profile, name="profile"),
]