# Generated by Django 3.1 on 2020-09-28 02:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0029_auto_20200928_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 1, 2, 49, 17, 824844, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]
