# Generated by Django 3.1 on 2020-10-06 10:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0048_auto_20201005_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 9, 10, 16, 58, 645069, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]