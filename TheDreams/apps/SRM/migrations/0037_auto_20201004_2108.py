# Generated by Django 3.1 on 2020-10-04 18:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0036_auto_20201004_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 7, 18, 8, 48, 821565, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]
