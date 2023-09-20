#!/usr/bin/env python
"""URL patterns for the views in newsletter app."""
from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.newsletter_list, name='newsletter_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.newsletter_detail, name='newsletter_detail'),
]