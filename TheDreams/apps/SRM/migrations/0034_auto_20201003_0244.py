# Generated by Django 3.1 on 2020-10-02 23:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0033_auto_20201001_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 5, 23, 44, 17, 30073, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]
