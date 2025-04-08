from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date_added')  # Fields to display in the list view
    search_fields = ('title', 'description') 