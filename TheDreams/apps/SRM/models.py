from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models

from datetime import datetime, timedelta

from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.utils.timezone import now

from changelog.signals import journal_save_handler, journal_delete_handler


def register_save_handler(class_object: object):
    post_save.connect(journal_save_handler, sender=class_object)


def register_delete_handler(class_object: object):
    post_save.connect(journal_delete_handler, sender=class_object)


class Order(models.Model):
    topic = models.CharField(max_length=150, verbose_name='Тема', blank=False, default='')

    task_from = models.ForeignKey(get_user_model(), related_name='task_from', verbose_name='От',
                                  on_delete=models.CASCADE)

    task_to = models.ManyToManyField(get_user_model(), related_name='task_to', verbose_name='Кому', blank=True)
    task_to_group = models.ManyToManyField(Group, related_name='task_to_group', verbose_name='Группе',
                                           blank=True)

    task_text = RichTextField(max_length=4200, verbose_name="Текст", default='')
    implementation_report = RichTextField(max_length=4200, verbose_name="Отчёт о выполнении", default='', blank=True)

    post_date = models.DateField(verbose_name="Дата размещения", default=now)
    deathline = models.DateField(verbose_name="Дедлайн", default=now() + timedelta(days=3))

    executed = models.BooleanField(verbose_name='Исполнено', default=False)

    def __str__(self):
        return f'{self.topic}'

    def get_users(self):
        return ", ".join([str(p) for p in self.task_to.all()])

    def get_groups(self):
        return ", ".join([str(p) for p in self.task_to_group.all()])

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


for item in [
    Order,

]:
    register_save_handler(class_object=item)
    register_delete_handler(class_object=item)
