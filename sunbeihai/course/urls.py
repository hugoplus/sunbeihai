#!/usr/bin/env python
"""URL patterns for the views in course app."""
from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('detail/<slug:slug>/', views.course_detail, name='course_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/comment/', views.article_comment, name='article_comment'),
    path('article/<int:article_id>/comments/', views.article_comment_list, name='article_comment_list'),
    path('comment/<int:article_id>/<int:comment_id>/', views.article_comment_detail, name='article_comment_detail'),
    path('comment/append/<int:article_id>/<int:parent_comment_id>/', views.article_comment_append, name='article_comment_append'),
    path('search/', views.article_search, name='article_search'),
    path('subscribe/', views.course_subscribe, name='course_subscribe')
]