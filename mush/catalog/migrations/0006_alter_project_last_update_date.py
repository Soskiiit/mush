# Generated by Django 3.2.18 on 2023-04-26 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_project_last_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата публикации'),
        ),
    ]
