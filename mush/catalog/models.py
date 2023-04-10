from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


class Project(models.Model):
    status_choices = (
        ('in_queue', 'в очереди'),
        ('in_progress', 'в обработке'),
        ('completed', 'обработка завершена'),
        ('error', 'ошибка')
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
    for_project = models.ForeignKey(
        Project, verbose_name='привязано к', on_delete=models.CASCADE
    )

    def get_img_1280x(self):
        return get_thumbnail(self.image, '1280', quality=51)

    def get_img_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def get_img_600x600(self):
        return get_thumbnail(self.image, '600x600', crop='center', quality=51)

    def img_thmb(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' width='50px'>")

    img_thmb.short_description = "превью"
    img_thmb.allow_tags = True

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return str(self.image).split('/')[-1]
