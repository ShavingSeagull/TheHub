import json
from django.core import serializers
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from .forms import CreateUserForm, EditUserForm

@login_required
@user_passes_test(lambda u:u.is_staff)
def admin_area(request):
    """
    Renders the admin area view. Provides a customised, user-friendly
    alternative to the Django admin panel. Only accessible to those
    with the is_staff flag (admin users).
    """
    return render(request, "administration/admin_area.html")

@login_required
@user_passes_test(lambda u:u.is_staff)
def create_user(request):
    """
    Allows a new user to be created without going through the Django
    admin panel. Allows the Profile model to register the user's
    first and last name on creation, unlike with the admin panel.
    Users will be created by a system admin, not by the new user themselves.
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = User.objects.make_random_password()
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            is_superuser = request.POST.get('is_superuser')
            associated_username = User.objects.filter(Q(username=username))
            associated_email = User.objects.filter(Q(email=email))

            if associated_username.exists():
                messages.error(request, "That username has already been taken.")
            elif associated_email.exists():
                messages.error(request, "That email address has already been taken.")
            else:
                if is_superuser:
                    new_user = User.objects.create_superuser(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                else:
                    new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                
                content = {
                    'name': new_user.first_name,
                    'email': new_user.email,
                    'password': password,
                    'url': request.build_absolute_uri(reverse('password_reset'))
                }
                subject = "The Hub User Registration"
                body = render_to_string(
                    "administration/email_templates/user_registration.txt",
                    content
                )
                try:
                    send_mail(
                        subject,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        [new_user.email],
                        fail_silently=False
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header")
                messages.success(request, "User has been successfully registered")
                return redirect('home')
        else:
            messages.error(request, "Form is not valid")
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'administration/create_user.html', context=context)

@login_required
@user_passes_test(lambda u:u.is_staff)
def edit_user(request):
    """
    Allows an admin user to edit another user's account details
    from within the site itself, rather than using the Django
    Admin panel.
    """
    # NEED TO FINISH OFF THE VIEW AND ENSURE IT EDITS CORRECTLY
    users = User.objects.all()

    if request.method == 'POST':
        pass
    else:
        form = EditUserForm()

    context = {
        'form': form,
        'users': users,
    }
    return render(request, "administration/edit_user.html", context=context)

@login_required
@user_passes_test(lambda u:u.is_staff)
def user_data_api(request, username):
    """
    Returns the dataset for current users, in order to edit details
    on the edit_user view. Checks if the request contains the header
    to denote it's AJAX - if not, it redirects. This prevents the
    user visiting the API URL manually and not sending an AJAX request.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Returns a JSON dataset of all users, with only the necessary fields that can be edited
        user = serializers.serialize(
            "json", 
            User.objects.filter(username=username),
            fields=('email', 'first_name', 'last_name', 'is_staff', 'is_active')
        )
        return JsonResponse(user, safe=False)
    else:
        messages.error(request, "Data must be returned via AJAX request on the Edit User page")
        return redirect('home')
