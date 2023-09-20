from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Course, Category, Article, Comment, Subscriber


"""
"""

User = get_user_model()

"""
"""

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'owner', 'created_at', 'updated_at', 'description']
    list_filter = ['owner']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['owner']
    ordering = ['created_at']

"""
"""

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'course']
    list_filter = ['course', 'order']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['created_at', 'order']

"""
"""

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_at', 'updated_at', 'published_at', 'status']
    list_filter = ['author', 'status', 'published_at']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['created_at']

"""
"""

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'article', 'parent', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'body']

"""
"""

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'created_at']