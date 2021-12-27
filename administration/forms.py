from django import forms
from django.contrib.auth.models import User


class CreateUserForm(forms.ModelForm):
    """
    A form for creating a new user based on the inbuilt
    Django User model. The Profiles app will create a
    profile for the new user automatically via signal.
    """
    class Meta:
        model = User
        exclude = ('id', 'groups', 'is_staff',
                   'user_permissions', 'last_login', 'password')

    def __init__(self, *args, **kwargs):
            """
            Add placeholders, remove auto-generated
            labels and set autofocus on first field
            """
            super().__init__(*args, **kwargs)

            # Most fields of the Django User model are optional by default.
            # The custom admin area requires that all fields be mandatory,
            # thus the 'required' attribute is set on all fields.
            for field in self.fields:
                self.fields[field].required = True
