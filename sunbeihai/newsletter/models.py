from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

"""
"""

User = get_user_model()

"""
Newsletter model
"""

class Newsletter(models.Model):
    """This is the newsletter model."""
    
    # The fields for Newsletter model.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    subject = models.CharField(max_length=125)
    slug = models.SlugField(
        max_length=125, 
        unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='newsletters')
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.DRAFT)
    file = models.FileField(
        upload_to='newsletters/%Y/%m/%d/',
        blank=True)
    body = models.TextField(
        null=True,
        blank=True)
    
    # The Meta data for Newsletter model.
    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at'])]
    
    # The methods for Newsletter model.
    def __str__(self):
        return self.subject
    
    def get_absolute_url(self) -> str:
        return reverse(
            'newsletter:newsletter_detail',
            kwargs={
                'year': self.published_at.year,
                'month': self.published_at.month,
                'day': self.published_at.day,
                'slug': self.slug
                })
