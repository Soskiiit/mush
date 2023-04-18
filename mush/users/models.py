from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import get_thumbnail


class User(AbstractUser):
    image = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        null=True,
        upload_to='avatars'
    )
    twitter = models.CharField(
        unique=True,
        verbose_name='twitter',
        blank=True,
        null=True,
        max_length=15
    )
    github = models.CharField(
        unique=True,
        verbose_name='github',
        blank=True,
        null=True,
        max_length=255
    )

    def profile_img_300x300(self):
        if self.image:
            return get_thumbnail(
                self.image, '300x300', crop='center', quality=51
            )

    class Meta:
        verbose_name = 'о пользователе'
        verbose_name_plural = 'о пользователях'
