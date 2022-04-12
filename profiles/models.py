from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    The model for the user profiles. Includes details not found in the inbuilt
    Django User model, with the exception of the user's name.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    job_title = models.CharField(max_length=40, blank=False, null=False)
    # start_date = models.DateField()

    def __str__(self) -> str:
        return self.user.username
    

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Function for creating or updating the user profile
    """
    if created:
        Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
    instance.profile.save()


class Note(models.Model):
    """
    Model for the notes that users can leave themselves on their profile.
    """
    prof_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
