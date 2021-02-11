from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField
from changelog.mixins import ChangeloggableMixin
from changelog.signals import journal_delete_handler, journal_save_handler
from .services.text_modifications import triad_format, triad_format_new_line
from django.utils.translation import gettext_lazy as _


class CustomUser(ChangeloggableMixin, AbstractUser):
    """Модель пользователя сайта с дополнительными полями"""
    # avatar = models.ImageField(upload_to='/static/uploads')
    first_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Имя')

    email = models.EmailField(unique=False, blank=True, verbose_name='Адрес электронной почты')
    phone = PhoneNumberField(null=False, blank=True, unique=False, verbose_name='Номер телефона')

    join_date = models.DateField(verbose_name='Дата вступления', default=now)

    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    timezone = TimeZoneField(display_GMT_offset=True, blank=False, default='Europe/Moscow', verbose_name='Часовой пояс')

    code = models.CharField(max_length=50, blank=True, null=True, default=None, verbose_name='Код подтверждения')

    phone_hidden = models.BooleanField(default=False, verbose_name='Номер скрыт')
    email_hidden = models.BooleanField(default=False, verbose_name='Почта скрыта')

    all_fame = models.PositiveIntegerField(verbose_name='Всего славы', default=0)
    pk_fame = models.PositiveIntegerField(verbose_name='Слава за убийство игроков', default=0)

    mob_fame = models.PositiveIntegerField(verbose_name='Слава за убийство мобов', default=0)
    gathering_fame = models.PositiveIntegerField(verbose_name='Слава за собирательство', default=0)
    craft_fame = models.PositiveIntegerField(verbose_name='Слава за крафтинг', default=0)

    def user_activity_get_names(self):
        """Получение списка в виде строки пользовательский активностей,
         выбранных в личном кабинете или при регистрации"""
        return " ".join([str(activity) for activity in UserActivity.objects.filter(user_activity=self.id)])

    def user_prime_time_names(self):
        """Получение списка в виде строки пользовательского прайм-тайма"""
        return ", ".join([str(prime_time) for prime_time in UserPrimeTime.objects.filter(user_prime_time=self.id)])

    class Meta:
        app_label = 'statistic'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class PrimeTime(models.Model):
    """Модуль времени основной активности пользователя"""
    prime_time = models.CharField(max_length=25, verbose_name='Прайм-тайм')
    beginning = models.TimeField(verbose_name="Начало", default=now)
    ending = models.TimeField(verbose_name="Конец", default=now)

    def __str__(self):
        return f'{self.prime_time}\n({self.beginning} - {self.ending}) по МСК'

    class Meta:
        verbose_name = 'прайм-тайм'
        verbose_name_plural = 'прайм-таймы'


class UserPrimeTime(models.Model):
    """Выбранные пользователями прайм-таймы"""
    prime_time = models.ForeignKey(PrimeTime, verbose_name='прайм-тайм', related_name='activity',
                                   on_delete=models.CASCADE, blank=True)
    user_prime_time = models.ManyToManyField(get_user_model(), related_name='user_prime_time',
                                             verbose_name='Пользователь')

    def __str__(self):
        return f"{self.prime_time}"

    def get_users(self):
        """Получение списка в виде строки пользователей, выбравыших тот или иной прайм-тайм"""
        return ",".join([str(p) for p in self.user_prime_time.all()])

    class Meta:
        verbose_name = 'пользовательский прайм-тайм'
        verbose_name_plural = 'пользовательские прайм-таймы'


# class Payment(ChangeloggableMixin, models.Model):
#     payer = models.ForeignKey(get_user_model(), related_name='payer', verbose_name='Кем', on_delete=models.CASCADE)
#     whom = models.ManyToManyField(get_user_model(), related_name='whom', verbose_name='Кому')
#     date = models.DateTimeField(verbose_name="Время выплаты", default=now)
#     payment_amount = models.PositiveIntegerField(verbose_name="Сумма", default=0)
#     comment = models.CharField(max_length=250, default='', verbose_name='Комментарий')
#
#     def get_whom(self):
#         # whom = ", ".join([str(p.username) for p in self.whom.all()])
#         return self.whom.all()
#
#     def get_whom_admin(self):
#         whom = " ".join([str(p.username) for p in self.whom.all()])
#         return triad_format_new_line(whom)
#
#     def __str__(self):
#         return "Кем - {}; Когда - {}; Сумма - {}".format(
#             self.payer, self.date, self.payment_amount)
#
#     def triad_payment_format(self):
#         self.payment_amount = triad_format(self.payment_amount)
#
#     class Meta:
#         verbose_name = 'выплата'
#         verbose_name_plural = 'выплаты'


# class PaymentAmount(models.Model):
#     payment = models.ForeignKey(Payment, verbose_name='выплата', on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Кому', on_delete=models.CASCADE)
#     payed = models.BooleanField(verbose_name='Уплачено')
#
#     def __str__(self):
#         return f"{self.payment.payer} - Дата: {self.payment.date} - Выплачено: {self.payed}"
#
#     class Meta:
#         unique_together = (("payment", "user"),)
#         verbose_name = 'подтверждение выплаты'
#         verbose_name_plural = 'подтверждение выплат'


class Activity(models.Model):
    """Модель пользовательских активностей"""
    activity_type = models.CharField(max_length=50, verbose_name="Тип активности", default='')

    def __str__(self):
        return self.activity_type

    def __unicode__(self):
        return self.activity_type

    class Meta:
        verbose_name = 'активность'
        verbose_name_plural = 'активности'


class Recruit(models.Model):
    """Модель гильдейских рекрутёров"""
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Рекрутёр', related_name='recruiter',
                                  on_delete=models.CASCADE, null=True)
    invitee = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Приглашенный', related_name='invitee')
    user_fame = models.PositiveIntegerField(verbose_name='Всего славы', default=0)
    week = models.DateField(default=now, verbose_name='Дата')

    def __str__(self):
        return f'Рекрутёр: {self.recruiter}    Дата: {self.week}'

    class Meta:
        verbose_name = 'рекрут'
        verbose_name_plural = 'рекруты'


class Mentor(models.Model):
    """Модель гильдейских менторов."""
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Ментор', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mentor}"

    def __unicode__(self):
        return f"{self.mentor}"

    class Meta:
        verbose_name = 'ментор'
        verbose_name_plural = 'менторы'


class Mentoring(models.Model):
    """Модель связывающая менторов и обучаемых новичков"""
    mentor = models.ForeignKey(Mentor, verbose_name='Ментор', on_delete=models.CASCADE)
    people = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Сопровождаемые')
    direction_of_development = models.ManyToManyField(Activity, verbose_name='Направления развития')

    def __str__(self):
        return f"Ментор: {self.mentor}"

    def get_users(self):
        """Возвращает списко в виде строки пользователей, закреплённых за ментором"""
        return ", ".join([str(p) for p in self.people.all()])

    class Meta:
        verbose_name = 'менторство'
        verbose_name_plural = 'менторство'


class UserActivity(models.Model):
    """Модель пользовательских активностей, выбранных в личном кабинете или при регистрации"""
    activity = models.ForeignKey(Activity, verbose_name='Активность', related_name='activity',
                                 on_delete=models.CASCADE, blank=True)
    user_activity = models.ManyToManyField(get_user_model(), verbose_name='Пользователь', related_name='user_activity')

    def __str__(self):
        return f"{self.activity}"

    def get_users(self):
        """Возвращаем список пользователей в виде строки, выбравших данную активность"""
        return ",".join([str(p) for p in self.user_activity.all()])

    class Meta:
        verbose_name = 'пользовательская активность'
        verbose_name_plural = 'пользовательские активности'


class About(models.Model):
    """Статистика гильдии и её описание"""
    name = models.CharField(default='', max_length=250, verbose_name='Название')
    alliance = models.CharField(max_length=100, verbose_name='Альянс', default='', blank=True)
    guild_id = models.CharField(default='', max_length=500, verbose_name='ID гильдии', blank=True)
    alliance_id = models.CharField(max_length=100, verbose_name='ID альянса', default='', blank=True)
    description = RichTextField(max_length=4200, verbose_name="Описание")
    kill_fame = models.PositiveBigIntegerField(verbose_name='Слава за убийства', default=0)
    death_fame = models.PositiveBigIntegerField(verbose_name='Славы за смерть', default=0)
    member_count = models.PositiveIntegerField(verbose_name='Количество участников', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Гильдия'
        verbose_name_plural = 'Гильдии'


class Role(models.Model):
    """Пользовательские роли"""
    role_name = models.CharField(max_length=25, verbose_name='Роль')

    def __str__(self):
        return f'{self.role_name}'

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'роли'


class UserRole(models.Model):
    """Пользовательские роли, выбарнные на странице личного кабинета"""
    role_name = models.ForeignKey(Role, verbose_name='роль', related_name='activity',
                                  on_delete=models.CASCADE, blank=True)
    user_role = models.ManyToManyField(get_user_model(), related_name='user_role', verbose_name='Пользователь')

    def __str__(self):
        return f"{self.role_name}"

    def get_users(self):
        """Возвращает список пользователей в виде строки, выбравших данную роль"""
        return ",".join([str(p) for p in self.user_role.all()])

    class Meta:
        verbose_name = 'пользовательская роль'
        verbose_name_plural = 'пользовательские роли'


def register_save_handler(registered_class: object):
    post_save.connect(journal_save_handler, sender=registered_class)


def register_delete_handler(registered_class: object):
    post_delete.connect(journal_delete_handler, sender=registered_class)


# Регистрация ивентов изменения объектво модели
for item in [
    CustomUser,
    Recruit,
    UserActivity,
]:
    register_save_handler(registered_class=item)
    register_delete_handler(registered_class=item)
