#!/usr/bin/env python
"""Custom tags fo account app."""

from django import template
from django.utils.translation import gettext_lazy as _

"""
"""

register = template.Library()

"""
"""

@register.simple_tag
def load_greeting_message():
    """Load greeting message."""
    return _("欢迎访问孙北海的官方网站！")

"""
"""

@register.inclusion_tag('account/tags/jump_count_down_js.html')
def load_jump_count_down_js(count_down_seconds=5, redirection_page="course:article_list"):
    """Load jump count down js."""
    
    return {
        "count_down_seconds": count_down_seconds,
        "redirection_page": redirection_page,
        }
    
"""
"""

@register.inclusion_tag('account/tags/jump_count_down_redirection_login.html')
def load_jump_count_down_redirection_login(count_down_seconds=5, redirection_page="account:login"):
    """Load jump count down redirection login."""
    
    return {
        "count_down_seconds": count_down_seconds,
        "redirection_page": redirection_page,
        }
    
"""
"""

@register.inclusion_tag('account/tags/jump_count_down_redirection_homepage.html')
def load_jump_count_down_redirection_homepage(count_down_seconds=5, redirection_page="course:article_list"):
    """Load jump count down redirection homepage."""
    
    return {
        "count_down_seconds": count_down_seconds,
        "redirection_page": redirection_page,
        }