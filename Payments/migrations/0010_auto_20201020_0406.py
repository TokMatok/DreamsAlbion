# Generated by Django 3.1 on 2020-10-20 01:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Payments', '0009_auto_20201006_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'выплата', 'verbose_name_plural': 'выплаты'},
        ),
        migrations.AddField(
            model_name='payment',
            name='treasurer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Payments.treasurer', verbose_name='Казначей'),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='whom',
        ),
        migrations.AddField(
            model_name='payment',
            name='whom',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, verbose_name='Кому'),
        ),
        migrations.DeleteModel(
            name='TreasurerPayment',
        ),
    ]
