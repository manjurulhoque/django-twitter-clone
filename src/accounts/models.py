import django
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    username = models.CharField(max_length=256, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=15, blank=True)
    website = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    profile_picture = models.ImageField(null=True,
                                        blank=True,
                                        upload_to='photos',
                                        default='images/default_profile.png',
                                        verbose_name="profile picture"
                                        )
    profile_cover = models.ImageField(null=True,
                                      blank=True,
                                      upload_to='photos',
                                      default='images/default_cover.png',
                                      verbose_name="profile cover"
                                      )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username
