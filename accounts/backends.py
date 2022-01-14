from django.contrib.auth import get_user_model
from django.db.models import Q

# The get_user_model method works with custom-set user auth models
User = get_user_model()


class CaseInsensitiveAuth:

    def authenticate(self, username_or_email=None, password=None):
        """
        Get an instance of User using the supplied username
        or email (case insensitive) and verify the password
        """
        # Filter all users by searching for a match by username/email.
        users = User.objects.filter(Q(username__iexact=username_or_email) |
                                    Q(email__iexact=username_or_email))
        if not users:
            return None

        user = users[0]
        # If the password checks out, return the user
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        """
        Used by the Django authentication system to retrieve a User instance
        """
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
