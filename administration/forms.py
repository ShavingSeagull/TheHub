from django import forms
from django.contrib.auth.models import User
from documents.models import Category


class CreateUserForm(forms.ModelForm):
    """
    A form for creating a new user based on the inbuilt
    Django User model. The Profiles app will create a
    profile for the new user automatically via signal.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                    'last_name', 'date_joined')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Most fields of the Django User model are optional by default.
        # The custom admin area requires that all fields be mandatory,
        # thus the 'required' attribute is set on all fields.
        for field in self.fields:
            self.fields[field].required = True

class EditUserForm(forms.ModelForm):
    """
    A form for editing an existing user based on the inbuilt
    Django User model. Key difference between the Edit and
    Create form is that the 'username' field is omitted.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True

class CreateEditCategoryForm(forms.ModelForm):
    """
    A form for creating a new category for document creation.
    """
    class Meta:
        model = Category
        fields = ('friendly_name',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True
