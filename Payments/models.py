from django.conf import settings
from django.db import models
from django.utils.timezone import now

from changelog.mixins import ChangeloggableMixin
from django.db.models.signals import post_save, post_delete
from changelog.signals import journal_delete_handler, journal_save_handler


class Treasurer(models.Model):
    treasurer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Казначей', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.treasurer}"

    class Meta:
        verbose_name = 'Казначей'
        verbose_name_plural = 'Казначеи'


class Payment(ChangeloggableMixin, models.Model):
    treasurer = models.ForeignKey(Treasurer, verbose_name='Казначей', null=True, on_delete=models.CASCADE)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='Кому', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата выплаты", default=now)
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма", default=0)
    comment = models.CharField(max_length=250, default='', verbose_name='За что произведена')
    confirm = models.BooleanField(default=False, verbose_name='Уплачено')

    def __str__(self):
        return f"Кому: {self.whom};Сумма: {self.payment_amount}; Дата: {self.date}"

    class Meta:
        verbose_name = 'выплата'
        verbose_name_plural = 'выплаты'


def register_save_handler(registered_class: object):
    post_save.connect(journal_save_handler, sender=registered_class)


def register_delete_handler(registered_class: object):
    post_delete.connect(journal_delete_handler, sender=registered_class)


for item in [
    Treasurer,
    Payment,
]:
    register_save_handler(registered_class=item)
    register_delete_handler(registered_class=item)
