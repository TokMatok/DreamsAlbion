# Generated by Django 3.1 on 2020-09-26 19:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0014_auto_20200926_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 9, 29, 22, 13, 59, 305848), verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='order',
            name='post_date',
            field=models.DateField(default=datetime.datetime(2020, 9, 26, 22, 13, 59, 305848), verbose_name='Дата размещения'),
        ),
    ]
