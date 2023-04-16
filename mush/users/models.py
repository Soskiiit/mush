from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import get_thumbnail


class UserProfile(models.Model):
    for_user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='пользователь'
    )
    image = models.ImageField(
        verbose_name='Аватар',
        blank=True,
        upload_to='avatars'
    )
    bio = models.CharField(verbose_name='О себе', max_length=256)

    def get_img_300x300(self):
        if self.image:
            return get_thumbnail(
                self.image, '300x300', crop='center', quality=51
            )
        else:
            return False

    class Meta:
        verbose_name = 'о пользователе'
        verbose_name_plural = 'о пользователях'

    def __str__(self):
        return str(self.for_user)
