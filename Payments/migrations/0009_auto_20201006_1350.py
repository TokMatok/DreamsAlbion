# Generated by Django 3.1 on 2020-10-06 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0008_auto_20201006_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treasurerpayment',
            old_name='users_payments',
            new_name='payments',
        ),
    ]
