from django.contrib import admin
from .models import ImageBookmark

@admin.register(ImageBookmark)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'thumbnail_tag', 'created']
    list_filter = ['created']