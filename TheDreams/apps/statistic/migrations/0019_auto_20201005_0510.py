# Generated by Django 3.1 on 2020-10-05 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0018_auto_20201004_2108'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paymentamount',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='paymentamount',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='paymentamount',
            name='user',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PaymentAmount',
        ),
    ]
