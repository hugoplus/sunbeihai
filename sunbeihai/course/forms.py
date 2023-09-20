#!/usr/bin/env python
"""Forms for the content in wiki."""
from django import forms
from django.forms import Textarea
from .models import Comment
from django.utils.translation import gettext_lazy as _

class CustomTextArea(Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        custom_attrs = {'class': 'form-control'}
        if attrs:
            custom_attrs |= attrs
        return super().render(name, value, custom_attrs)


class CommentForm(forms.ModelForm):
    """This is the form for the Comment model."""

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        labels = {
            'name': _('姓名'),
            'email': _('电子邮箱'),
            'body': _('评论')}

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'name@example.com', 'style': 'width:50%;'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),}