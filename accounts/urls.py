from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login, logout, ResetPasswordView

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('password-reset', ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
