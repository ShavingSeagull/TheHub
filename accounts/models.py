from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class GoogleOauthCredentials(models.Model):
    """
    Credentials gained from Google's authentication procedure
    are stored in the DB, as recommended by Google. For security
    purposes, this model is not registered in the admin panel.
    A full Google creds dictionary also requires the scopes needed, but
    these are set in the corresponding view and will be added from there.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)
    token_uri = models.CharField(max_length=255, null=True)
    client_id = models.CharField(max_length=255, null=True)
    client_secret = models.CharField(max_length=255, null=True)


@receiver(post_save, sender=User)
def create_google_creds_connection(sender, instance, created, **kwargs):
    """
    Function for creating or updating the user's Google auth creds
    """
    if created:
        GoogleOauthCredentials.objects.create(user=instance)
    instance.googleoauthcredentials.save()
