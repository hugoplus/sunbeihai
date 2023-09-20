from django.db import models
from django.contrib.auth.models import AbstractUser

"""
Sunbeihai website user model
"""

class SWUser(AbstractUser):
    """This is the custom user model for the Sunbeihai website."""
    
    # Roles for the user
    ADMINISTRATOR = 'administrator'
    AUTHOR = 'author'
    EDITOR = 'editor'
    READER = 'reader'
    PARTNER = 'partner'
    ROLES = (
        (ADMINISTRATOR, 'Administrator'),
        (AUTHOR, 'Author'),
        (EDITOR, 'Editor'),
        (READER, 'Reader'),
        (PARTNER, 'Partner')
    )
    
    # Fields for the user
    date_of_birth = models.DateField(
        blank=True,
        null=True
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True
    )
    role = models.CharField(
        max_length=100,
        choices=ROLES,
        default=AUTHOR
    )
    
    # Methods for the user
    def __str__(self):
        return f'Profile for user {self.username}'

