# Generated by Django 3.1 on 2020-09-28 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0013_mentor_mentoring'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='FAQ',
        ),
    ]
