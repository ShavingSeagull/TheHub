from django.db import models


class Category(models.Model):
    """
    The model for the document categories.
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    The models for the document tags.
    """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Document(models.Model):
    """
    The model for a Google Doc/Sheet that
    holds all of its info.
    """
