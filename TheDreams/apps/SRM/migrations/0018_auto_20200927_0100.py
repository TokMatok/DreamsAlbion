# Generated by Django 3.1 on 2020-09-26 22:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0017_auto_20200927_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 9, 30, 1, 0, 38, 688671), verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='order',
            name='post_date',
            field=models.DateField(default=datetime.datetime(2020, 9, 27, 1, 0, 38, 688671), verbose_name='Дата размещения'),
        ),
    ]
