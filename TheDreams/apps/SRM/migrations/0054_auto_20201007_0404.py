# Generated by Django 3.1 on 2020-10-07 01:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0053_auto_20201006_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 10, 1, 4, 35, 641852, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]