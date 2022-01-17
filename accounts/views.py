from operator import concat
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserLoginForm


User = get_user_model()

def login(request):
    """
    Function to authenticate the user and log them in.
    """
    next_page = request.GET.get('next') or reverse('home')
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(login_form.cleaned_data['email_or_username'],
                                password=login_form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return redirect(next_page)
            else:
                login_form.add_error(
                    None, "Your username or password are incorrect")
    else:
        login_form = UserLoginForm()

    return render(request, 'accounts/login.html',
                  {'form': login_form, 'next': next_page})

def logout(request):
    """
    Logs the user out.
    """
    auth.logout(request)
    return redirect('login')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Extends the inbuilt PasswordResetView to customise the templates and email messages used.
    The inbuilt views are class-based.
    """
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/email_templates/password_reset_email.txt'
    subject_template_name = 'accounts/email_templates/password_reset_subject.txt'
    success_message = concat("You have been emailed instructions for setting your new password. ",
        "If the email doesn't come through, check the address that was used and also check your spam folder.")
    success_url = reverse_lazy('login')
