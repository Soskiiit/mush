import os

from django.db import models
from django.forms import ValidationError
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from users.models import User


class Project(models.Model):
    name = models.CharField(verbose_name='название', max_length=255)
    owner = models.ForeignKey(
        User, verbose_name='владелец', on_delete=models.CASCADE
    )
    is_public = models.BooleanField(default=False, verbose_name='публичный')
    model = models.OneToOneField(
        'Model3D',
        on_delete=models.CASCADE,
        null=True
    )
    preview = models.OneToOneField(
        'Photo',
        verbose_name='Превью',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    last_update_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    image = models.ImageField(upload_to='gallery', verbose_name='изображение')
    for_model = models.ForeignKey(
        'Model3D',
        verbose_name='привязано к',
        on_delete=models.CASCADE,
        related_name='photos',
    )

    def get_img_1280x(self):
        return get_thumbnail(self.image, '1280', quality=51)

    def get_img_300x300(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def get_img_600x600(self):
        return get_thumbnail(self.image, '600x600', crop='center', quality=51)

    def img_thmb(self):
        if self.image:
            return mark_safe(f'''<img src='{self.image.url}' width='50px'>''')

    img_thmb.short_description = 'превью'
    img_thmb.allow_tags = True

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return f'{os.path.basename(str(self.image))}'


class Model3D(models.Model):
    status_choices = (
        ('empty', 'пуст'),
        ('in_queue', 'в очереди'),
        ('in_progress', 'в обработке'),
        ('completed', 'обработка завершена'),
        ('error', 'ошибка')
    )
    status = models.CharField(
        choices=status_choices, default='empty', max_length=255
    )
    original = models.FileField(
        upload_to='models_highres',
        verbose_name='3D модель',
        null=True,
        blank=True,
    )
    lowres = models.FileField(
        upload_to='models_lowres',
        verbose_name='3D модель (LOD in .glb)',
        null=True,
        blank=True,
    )
    face_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Число полигонов'
    )
    vertex_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Число вершин'
    )

    def extension(self):
        return os.path.splitext(str(self.original))[1]
    extension.short_description = 'Расширение модели'

    def file_size(self):
        return os.path.getsize(self.original.path) if self.original else 0
    file_size.short_description = 'Размер файла модели'

    def clean(self):
        if bool(self.original) != bool(self.lowres):
            raise ValidationError(
                'Model3D must have both original and lowres models set ot none'
            )

    def __str__(self):
        if self.original:
            return f'{os.path.basename(self.original.name)}'
        return 'From images'

    class Meta:
        verbose_name = '3D Модель'
        verbose_name_plural = '3D Модели'
