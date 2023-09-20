#!/usr/bin/env python
"""Custom tags fo course app."""
from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import markdown
from ..models import Article, Category, Course

"""
"""

register = template.Library()

"""
"""

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['markdown.extensions.extra', 'pymdownx.superfences', 'markdown.extensions.codehilite', 'pymdownx.betterem', 'pymdownx.inlinehilite', 'pymdownx.highlight']))

@register.inclusion_tag('course/navbar.html')
def show_nav_bar(current_item=-1):
    courses = Course.published_objects.all()
    return {
        'courses': courses,
        'current_course_id': current_item
    }

@register.inclusion_tag('course/treeview.html')
def show_treeview(content_tree, article_title):
    return {
        'content_tree': content_tree,
        'article_title': article_title
    }

@register.simple_tag
def show_comment_quantity(article_id):
    article = Article.objects.get(id=article_id)
    if article.comments.count() == 0:
        return _("目前，评论区尚没有评论。")
    else:
        return _(f"目前，评论区共有 {article.comments.count()} 条评论。")

@register.filter(name='is_list')
def is_list(value):
    return isinstance(value, list)

@register.filter(name='first_item')
def first_item(items):
    return items[0]

@register.filter(name='last_item')
def last_item(items):
    return items[-1]

@register.filter(name='remaining_items')
def remaining_items(items, start_from=1):
    return items[start_from:]

@register.filter(name='list_length')
def list_length(items):
    return len(items)