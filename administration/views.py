from django.shortcuts import render
from .forms import CreateUserForm

def admin_area(request):
    """
    Renders the admin area view. Provides a customised, user-friendly
    alternative to the Django admin panel.
    """
    return render(request, "administration/admin_area.html")

def create_user(request):
    """
    Allows a new user to be created without going through the Django
    admin panel. Allows the Profile model to register the user's
    first and last name on creation, unlike with the admin panel.
    """
    
    # HOOK THE TOGGLE BUTTONS UP VIA JS!

    if request.method == 'POST':
        pass
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }

    return render(request, 'administration/create_user.html', context=context)
