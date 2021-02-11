import random
import threading
from datetime import timedelta
from logging import getLogger

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from changelog.templatetags.custom_template_tag import is_group
from . import forms
from .forms import CustomUserCreationForm, RecruitForm, MyActivationCodeForm, UserEdit
from .models import About, Recruit, UserPrimeTime, UserActivity, UserRole

logger = getLogger(__name__)


# Блок обработчиков исключений
# Переопределенный метод 404 exception
def bad_request(request, exception):
    print(exception)
    return render(request, 'bad_request.html',
                  context={"page_title": 'Неверный запрос'})


# Переопределенный метод 404 exception
def page_not_found(request, exception):
    print(exception)
    return render(request, '404.html',
                  context={"page_title": 'Страница не найдена'})


# Переопределенный метод 403 exception
def permission_denied(request, exception):
    print(exception)
    return render(request, 'permission_denied.html',
                  context={"page_title": 'Недостаточно прав'})


# Переопределенный метод 500 exception
def server_error(request):
    return render(request, 'server_error.html',
                  context={"page_title": 'Ошибка сервера'})


# Блок основного контента

def index(request):
    """ Главная страница сайта """

    # Выгрузка данных, собранных на albion-data-online о текущей гильдии
    guild_about = About.objects.filter(guild_id=settings.GUILD_ID)

    # Виджет гильдейских ролей и их участников
    groups = {}
    for group_ in Group.objects.all():
        user = get_user_model().objects.filter(groups__name=group_)
        groups.update({group_.name: user})

    # Проверка наличия статистики о гильдии
    if guild_about:
        guild_about = guild_about[0]

    # About гильдии
    about = About.objects.filter(guild_id=settings.GUILD_ID)

    # Проверка налигия about гильдии
    if about:
        about = about[0]

    return render(request, 'Statistic/index.html',
                  context={"page_title": 'The Dreams Albion',
                           'guild_about': guild_about,
                           'about': about,
                           'groups': groups,
                           })


def top(request):
    # Выгрузка всех пользователей для составления топа
    users = get_user_model().objects.all()

    # Список лидеров по общему количеству славы
    top_fame = users.order_by('-all_fame')[:10]

    # Список лидеров по ублийству игроков
    pk_fame = users.order_by('-pk_fame')[:10]

    # Список лидеров по ублийству мобов
    mob_fame = users.order_by('-mob_fame')[:10]

    # Список лидеров по собирательству
    gathering_fame = users.order_by('-gathering_fame')[:10]

    # Список лидеров по крафту
    craft_fame = users.order_by('-craft_fame')[:10]

    return render(request=request,
                  template_name="Statistic/tops.html",
                  context={'top_fame': top_fame,
                           'pk_fame': pk_fame,
                           'mob_fame': mob_fame,
                           'gathering_fame': gathering_fame,
                           'craft_fame': craft_fame,
                           "page_title": 'Топы'})


# Блок офирского крыла


def required_add(request):
    """ Старница добавления новых рекрутов в гильдию """

    # Проверка на нахождение пользователя в группе рекрутёров
    if not is_group(request.user, 'Рекрутёр') and not is_group(request.user, 'admin'):
        # Редирект на граную страницу, если пользователь не рекрутёр
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RecruitForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Успешно')
                return render(request, 'Statistic/required_add.html',
                              context={"page_title": 'Добавить рекрут', 'form': form})
            else:
                return render(request, 'Statistic/required_add.html',
                              context={"page_title": 'Добавить рекрут', 'form': form})
        else:
            form = RecruitForm()
            return render(request, 'Statistic/required_add.html',
                          context={"page_title": 'Добавить рекрут', 'form': form})


def required_admin(request):
    # if not is_group(request.user, "Глава рекрутёров"):
    #     return redirect('/')
    # else:
    #     weeks = {}
    #     recruit = Recruit.objects.all()
    #     for i in recruit:
    #         week = i.week.isocalendar()[1]
    #         if i.week.isocalendar()[1] not in weeks:
    #             weeks.update({week: [i]})
    #         else:
    #             weeks[week].append(i)
    #
    #     return render(request, 'Statistic/required_admin.html',
    #                   context={"page_title": 'Админка рекрута', 'weeks': weeks})
    return redirect('/')


class RecruitCreateView(generic.CreateView):
    model = Recruit
    form_class = forms.RecruitForm
    success_url = "/"


# Блок авторизации, регистрации и личного кабинета


def profile(request, user_name):
    this_user = get_user_model().objects.filter(username=user_name)
    error = False
    max_table_length = 0
    if this_user:
        this_user = this_user[0]
        max_table_length = max([
            len(this_user.user_prime_time.all()),
            len(this_user.user_activity.all()),
            len(this_user.user_prime_time.all())])

    else:

        error = 'Пользователь не найден'

    return render(request,
                  template_name='account/account.html',
                  context={
                      "page_title": f'Профиль {user_name}',
                      'error': error,
                      'this_user': this_user,
                      'max_table_length': range(max_table_length)
                  })


def group(request, group_name):
    this_group = Group.objects.filter(name=group_name)
    users = get_user_model().objects.filter(groups__name=group_name)
    if this_group:
        this_group = this_group[0]
    return render(request,
                  template_name='account/groups.html',
                  context={
                      "page_title": f'Группа {this_group}',
                      'this_group': this_group,
                      'users_in_group': users
                  })


def user_profile(request):
    max_table_length = 0
    max_table_length = max([
        len(request.user.user_prime_time.all()),
        len(request.user.user_activity.all()),
        len(request.user.user_prime_time.all())])
    return render(request,
                  template_name='account/account.html',
                  context={
                      "page_title": f'Мой профиль',
                      'this_user': request.user,
                      'max_table_length': range(max_table_length)

                  })


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            my_password1 = form.cleaned_data.get('password1')
            code = generate_code()
            user = authenticate(username=username, password=my_password1)
            html_message = render_to_string('mail_template.html', {'code': code, 'user': user})
            plain_message = strip_tags(html_message)
            message = plain_message
            user.code = code
            user.is_active = False
            user.save()
            send_mail(subject='Завершение регистрации',
                      message=message,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[form.cleaned_data.get('email')],
                      html_message=html_message,
                      fail_silently=True)
            if user and not user.is_active:
                login(request, user)
                return redirect('/activation_code_form')
            else:
                form.add_error(None, 'Unknown or disabled account')
                return render(request, template_name='account/register.html',
                              context={'form': form, "page_title": 'Регистрация'})

        else:
            return render(request=request,
                          template_name="account/register.html",
                          context={"form": form, "page_title": 'Регистрация'})

    form = CustomUserCreationForm()
    return render(request=request,
                  template_name="account/register.html",
                  context={"form": form, "page_title": 'Регистрация'})


def end_reg(request):
    if not request.user.is_active:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if get_user_model().objects.filter(code=code_use):
                    user = get_user_model().objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'account/activation_code_form.html',
                                  {'form': form, "page_title": 'Активация'})
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'account/activation_code_form.html',
                                  {'form': form, "page_title": 'Активация'})
            else:
                return render(request, 'account/activation_code_form.html', {'form': form, "page_title": 'Активация'})
        else:
            form = MyActivationCodeForm()
            return render(request, 'account/activation_code_form.html', {'form': form, "page_title": 'Активация'})

    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/')


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request=request,
                          template_name="account/login.html",
                          context={"form": form, "page_title": 'Вход'})

    else:
        form = AuthenticationForm()
        return render(request=request,
                      template_name="account/login.html",
                      context={"form": form, "page_title": 'Вход'})


def change_user(request):
    """Страница редактирования личного профиля"""
    if request.method == 'POST':
        form = UserEdit(request.POST)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['first_name']:
                user.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
            if form.cleaned_data['phone']:
                user.phone = form.cleaned_data['phone']
            if form.cleaned_data['city']:
                user.city = form.cleaned_data['city']
            if form.cleaned_data['phone_hidden_fields']:
                user.phone_hidden = form.cleaned_data['phone_hidden_fields']
            if form.cleaned_data['email_hidden_fields']:
                user.email_hidden = form.cleaned_data['email_hidden_fields']
            if form.cleaned_data['prime_time_fields']:
                user_prime_times = UserPrimeTime.objects.filter(id__in=form.cleaned_data['prime_time_fields'])
                user.user_prime_time.set(user_prime_times)
            if form.cleaned_data['activity_fields']:
                user_activity = UserActivity.objects.filter(id__in=form.cleaned_data['activity_fields'])
                user.user_activity.set(user_activity)
            if form.cleaned_data['role_fields']:
                user_role = UserRole.objects.filter(id__in=form.cleaned_data['role_fields'])
                if user_role.filter(role_name__role_name__startswith='Nothing'):
                    user.user_role.clear()
                else:
                    user.user_role.set(user_role)

            user.timezone = form.cleaned_data['timezone']

            user.save()

        return render(request=request,
                      template_name="account/change_user.html",
                      context={"form": form, "page_title": 'Личный кабинет'}
                      )
    else:
        user = request.user
        if user.is_authenticated:
            # Предопределение полей
            form = UserEdit(initial={
                'first_name': request.user.first_name,
                'email': request.user.email,
                'phone': request.user.phone,
                'city': request.user.city,
                'phone_hidden_fields': request.user.phone_hidden,
                'email_hidden_fields': request.user.email_hidden,
                'prime_time_fields': [item for item in request.user.user_prime_time.values_list('id', flat=True)],
                'activity_fields': [item for item in request.user.user_activity.values_list('id', flat=True)],
                'role_fields': [item for item in request.user.user_role.values_list('id', flat=True)],
            })

            return render(request=request,
                          template_name="account/change_user.html",
                          context={"form": form, "page_title": 'Личный кабинет'}
                          )
        else:
            return redirect('/')


def mail_template(request):
    """Страница шаблона для исходнящих почтовых писем"""
    if request.user.is_staff:
        return render(request=request,
                      template_name="mail_template.html",
                      context={'code': 42612, 'user': request.user}
                      )
    else:
        return redirect('/')


def organisation(request, organisation_name):
    """В разработке"""
    if request.user.is_staff:
        activity = UserActivity.objects.filter()

        return render(request=request,
                      template_name="Statistic/organisation.html",
                      context={"page_title": 'Организация'})
    else:
        return redirect('/')
