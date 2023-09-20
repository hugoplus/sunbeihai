#!/usr/bin/env python
"""Sitemaps for the articles in course."""
from django.contrib.sitemaps import Sitemap
from .models import Article

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Article.published_objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at