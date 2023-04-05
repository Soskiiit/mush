# Generated by Django 3.2.18 on 2023-04-05 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('is_public', models.BooleanField(default=False, verbose_name='публичный')),
                ('status', models.CharField(choices=[('in_queue', 'в очереди'), ('in_progress', 'в обработке'), ('completed', 'обработка завершена')], default='in_queue', max_length=255)),
                ('models_highres', models.FileField(blank=True, null=True, upload_to='models_highres', verbose_name='3D модель')),
                ('model_lod', models.FileField(blank=True, null=True, upload_to='models_lod', verbose_name='3D модель (LOD in .glb)')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'проект',
                'verbose_name_plural': 'проекты',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery', verbose_name='изображение')),
                ('for_project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.project', verbose_name='привязано к')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
            },
        ),
    ]
