from tabnanny import verbose
from django.db import models


class Category(models.Model):
    """
    The model for the document categories.
    """
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    name = models.CharField(max_length=40)
    friendly_name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name


class Tag(models.Model):
    """
    The models for the document tags.
    """
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
