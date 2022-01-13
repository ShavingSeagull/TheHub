from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from .forms import CreateUserForm

@login_required
def admin_area(request):
    """
    Renders the admin area view. Provides a customised, user-friendly
    alternative to the Django admin panel.
    """
    return render(request, "administration/admin_area.html")

@login_required
def create_user(request):
    """
    Allows a new user to be created without going through the Django
    admin panel. Allows the Profile model to register the user's
    first and last name on creation, unlike with the admin panel.
    Users will be created by a system admin, not by the new user themselves.
    """
    if request.user:
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
                        'url': request.build_absolute_uri('accounts/password/reset/'),
                        'username': new_user.username,
                        'email': new_user.email
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
