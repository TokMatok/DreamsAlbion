# Generated by Django 3.1 on 2020-10-05 02:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('SRM', '0038_auto_20201005_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deathline',
            field=models.DateField(default=datetime.datetime(2020, 10, 8, 2, 12, 49, 3575, tzinfo=utc), verbose_name='Дедлайн'),
        ),
    ]
