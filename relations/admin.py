
from django.contrib import admin
from .models import Action, Contact


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to',  'created')
    list_filter = ('created',)
    search_fields = ('user_from', 'user_to', )