# Generated by Django 3.1 on 2020-09-06 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changelog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='data',
            field=models.JSONField(default=dict, verbose_name='Изменяемые данные модели'),
        ),
    ]
