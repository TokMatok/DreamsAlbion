from ckeditor.fields import RichTextField
from django.db import models
from django.utils.timezone import now

from changelog.mixins import ChangeloggableMixin
from django.db.models.signals import post_save, post_delete
from changelog.signals import journal_delete_handler, journal_save_handler


class New(ChangeloggableMixin, models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    text = RichTextField(max_length=4200, verbose_name="Текст")
    footer = RichTextField(max_length=200, verbose_name="Подвал", default='')
    pub_date = models.DateTimeField(verbose_name="Дата публикации", default=now)
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    reminder = models.CharField(max_length=150, verbose_name='Небольшая пометка', default='', blank=True)

    def __str__(self):
        return f"{self.title}"

    def __unicode__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class FAQ(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    text = RichTextField(max_length=4200, verbose_name="Текст")
    pub_date = models.DateTimeField(verbose_name="Дата публикации", default=now)
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    reminder = models.CharField(max_length=150, verbose_name='Небольшая пометка', default='', blank=True)

    def __str__(self):
        return f"{self.title}"

    def __unicode__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = "FAQ's"


def register_save_handler(item: object):
    post_save.connect(journal_save_handler, sender=item)


def register_delete_handler(item: object):
    post_delete.connect(journal_delete_handler, sender=item)


for item in [
    FAQ,
    New,
]:
    register_save_handler(item=item)
    register_delete_handler(item=item)
