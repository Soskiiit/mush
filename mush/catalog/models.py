import os

from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from users.models import User


class Project(models.Model):
    class ProgressOfProcessing(models.TextChoices):
        IN_QUEUE = 'in_queue', 'в очереди'
        IN_WORK = 'in_work', 'в обработке'
        COMPLETED = 'completed', 'обработка завершена'
        ERROR = 'error', 'ошибка'

    name = models.CharField(verbose_name='название', max_length=255)
    description = models.TextField(verbose_name='описание', blank=True)
    owner = models.ForeignKey(
        User, verbose_name='владелец', on_delete=models.CASCADE
    )
    is_public = models.BooleanField(default=False, verbose_name='публичный')
    status = models.CharField(
        choices=ProgressOfProcessing.choices,
        default=ProgressOfProcessing.IN_QUEUE,
        max_length=255
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
    preview = models.OneToOneField(
        'Photo',
        verbose_name='Превью',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    faces = models.IntegerField(default=0, verbose_name='Число полигонов')
    vertexes = models.IntegerField(default=0, verbose_name='Число вершин')
    public_date = models.DateField(auto_now_add=True,
                                   verbose_name='дата публикации')

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
            micro_image = get_thumbnail(
                self.image,
                '75x75',
                crop='center',
                quality=51
            )
            return mark_safe(f'''<img src='{micro_image.url}' width='75px'>''')

    img_thmb.short_description = 'превью'
    img_thmb.allow_tags = True

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return f'{os.path.basename(str(self.image))}'
