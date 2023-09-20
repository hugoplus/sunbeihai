from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Newsletter


"""
"""

User = get_user_model()

"""
"""

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'slug', 'author', 'created_at', 'published_at']
    list_filter = ['author', 'created_at', 'published_at']
    search_fields = ['subject', 'body']
    prepopulated_fields = {'slug': ('subject',)}
    raw_id_fields = ['author']
    ordering = ['created_at']