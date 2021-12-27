from django.shortcuts import render

def view_profile(request):
    """
    Renders the user's profile.
    """
    context = {
        'current_user': request.user,
        'first_name': request.user.profile.first_name
    }
    return render(request, "profiles/view_profile.html", context=context)
