# Generated by Django 3.1 on 2020-10-04 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0017_auto_20201003_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpayment',
            name='payments',
        ),
        migrations.RemoveField(
            model_name='userpayment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='UserPayment',
        ),
    ]