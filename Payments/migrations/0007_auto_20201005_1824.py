# Generated by Django 3.1 on 2020-10-05 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0006_auto_20201005_0704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpayment',
            options={'verbose_name': 'Выплата игроку', 'verbose_name_plural': 'Выплаты игрокам'},
        ),
    ]