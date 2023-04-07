import os

from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import get_thumbnail


class Project(models.Model):
    status_choices = (
        ('in_queue', 'в очереди'),
        ('in_progress', 'в обработке'),
        ('completed', 'обработка завершена'),
    )
    name = models.CharField(verbose_name='название', max_length=255)
    description = models.TextField(verbose_name='описание', blank=True)
    owner = models.ForeignKey(
        User, verbose_name='владелец', on_delete=models.CASCADE
    )
    is_public = models.BooleanField(default=False, verbose_name='публичный')
    status = models.CharField(
        choices=status_choices, default='in_queue', max_length=255
    )
    models_highres = models.FileField(
        upload_to='models_highres',
        verbose_name='3D модель',
        null=True,
        blank=True,
    )
    model_lod = models.FileField(
        upload_to='models_lod',
        verbose_name='3D модель (LOD in .glb)',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    image = models.ImageField(upload_to='gallery', verbose_name='изображение')
    for_project = models.OneToOneField(
        Project, verbose_name='привязано к', on_delete=models.CASCADE
    )

    def get_img_1280x(self):
        return get_thumbnail(self.image, '1280', quality=51)

    def get_img_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def get_img_600x600(self):
        return get_thumbnail(self.image, '600x600', crop='center', quality=51)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return f'{os.path.basename(self.image)}'
