# Generated by Django 3.2.18 on 2023-04-20 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_project_download_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='preview',
        ),
    ]
