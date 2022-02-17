from tabnanny import verbose
from django.db import models


class Category(models.Model):
    """
    The model for the document categories.
    """
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    The models for the document tags.
    """
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# class Document(models.Model):
#     """
#     The model for a Google Doc/Sheet that
#     holds all of the info neccessary to store
#     outside of Google. Most info will be retrieved
#     from the document's metadata on Google. This is
#     primarily for data not stored in the Google 
#     metadata, such as tags and categories. Other fields
#     are primarily for document identification.
#     """
#     doc_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
#     web_view_link = models.URLField(max_length=255, null=False, blank=False)
#     title = models.CharField(max_length=100, null=False, blank=False)
#     category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='doc_category', null=True, blank=True)
#     tags = models.ManyToManyField(Tag, related_name='doc_tags', null=True, blank=True)

