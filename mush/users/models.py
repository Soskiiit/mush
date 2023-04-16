from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    twitter = models.CharField(unique=True,
                               verbose_name='twitter',
                               max_length=15)
    github = models.CharField(unique=True,
                              verbose_name='github',
                              max_length=255)
    bio = models.CharField(verbose_name='О себе', max_length=256)
    
    def __str__(self):
        return str(self.username)
