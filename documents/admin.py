from django.contrib import admin
from django.contrib import admin
from .models import Category, Tag

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
