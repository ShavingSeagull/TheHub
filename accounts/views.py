from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model
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
