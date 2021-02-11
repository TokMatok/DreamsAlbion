import re
import datetime

import typing
from django import template
from django.contrib.auth.models import Group
from math import trunc

from django.db.models import Sum
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from Payments.models import Payment

register = template.Library()


@register.filter(name='is_group')
def is_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


@register.filter(name='triad_format')
def triad_format(s):
    return " ".join([str(s)[max(i - 3, 0):i] for i in range(len(str(s)), 0, -3)][::-1])


@register.simple_tag
def weeks_filter(weeks, week):
    this_element = weeks[week]
    week_start = this_element[0].week - datetime.timedelta(days=this_element[0].week.weekday())
    week_end = week_start + datetime.timedelta(days=6)
    week_start_and_end = f'{week_start} - {week_end}'
    recruits = [{'recruiter': i.recruiter, 'fame': i.user_fame, 'invitee': [a.username for a in i.invitee.all()]} for i
                in this_element]
    recruiter = {}
    for i in this_element:
        if i.recruiter not in register:
            recruiter.update({'invitee': [a.username for a in i.invitee.all()]})
            recruiter.update({'fame': i.user_fame})

    html = ''
    for i in recruits:
        html += '''< table class ="table table-dark table-striped table-hover table-sm " >
                        <thead>
                    <tr style="color: #00B0E8">
                        <th scope="col">#</th>
                        <th scope="col">Имя</th>
                        <th scope="col">Всего славы</th>
                        <th scope="col">убийство игроков</th>
                        <th scope="col">убийство мобов</th>
                        <th scope="col">собирательство</th>
                        <th scope="col">крафтинг</th>
                    </tr>
                    </thead>
                    <tbody>
        
        '''

    # return format_html_join('\n', "<h3>{}</h3> <br> {}", ((week_start_and_end, users),))


@register.filter(name='millennium_format')
def millennium_format(s: int):
    int_s = int(s)
    s = str(s)
    if 4 < len(s) <= 6:
        a = '{:,}'.format(trunc(int_s))
        return f"{a:1.5} k".replace(',', '.')
    if 7 <= len(s) <= 9:
        a = '{:,}'.format(trunc(int_s))
        return f"{a:1.5} m".replace(',', '.')
    if 10 <= len(s) <= 12:
        a = '{:,}'.format(trunc(int_s))
        return f"{a:1.5} b".replace(',', '.')
    if 13 <= len(s) <= 15:
        a = '{:,}'.format(trunc(int_s))
        return f"{a:1.5} t".replace(',', '.')

    if 16 <= len(s):
        a = '{:,}'.format(trunc(int_s))
        return f"{a:1.5} q".replace(',', '.')
    else:
        return triad_format(s)


@register.filter(name='dict_key')
def dict_key(d: dict, k: str):
    '''Returns the given key from a dictionary.'''
    return [i for i in d[k].all()]


@register.filter(name='search_user_call')
def search_user_call(text: str):
    if '@' in text:
        searched_users_calls: typing.List[str] = re.findall(r'(@[a-zа-яА-ЯA-Z0-9]+)', text)
        for i in searched_users_calls:
            user_call = i.split('@')[-1]
            groups_calls = Group.objects.filter(name=user_call)
            if groups_calls:
                user_link = f'<a target="_blank" href="/groups/{user_call}" style="color:#fafafa">{i}</a>'
            else:
                user_link = f'<a target="_blank" href="/account/{user_call}" style="color:#fafafa">{i}</a>'
            text = text.replace(i, user_link)
    if '&copy;' in text:
        searched_users_calls: typing.List[str] = re.findall('(&copy;[a-zа-яА-ЯA-Z0-9]+)', text)
        for i in searched_users_calls:
            user_call = i.split('&copy;')[-1]
            user_link = f'<a target="_blank" href="/account/{user_call}" style="color:#fafafa">{i}</a>'
            text = text.replace(i, user_link)

    return text


@register.simple_tag
def separate(text, length):
    if len(text) > length:
        return mark_safe(text[:length] + ' ...')
    else:
        return text


@register.filter
def index(item, i):
    try:
        return item[i]
    except IndexError:
        return ''


@register.filter
def outstanding_payments(user):
    if user:
        outstanding = Payment.objects.filter(whom=user, confirm=False).aggregate(
            Sum('payment_amount'))['payment_amount__sum']

        return outstanding if outstanding else 0
    else:
        return None


@register.filter
def completed_payments(user):
    if user:
        outstanding = Payment.objects.filter(whom=user, confirm=True).aggregate(
            Sum('payment_amount'))['payment_amount__sum']

        return outstanding if outstanding else 0
    else:
        return None


@register.filter
def load_payments(user):
    payments = Payment.objects.filter(whom=user, confirm=True)
    return payments if payments else []


@register.filter
def max_user_columns(user):
    if user:
        return range(max([
            len(user.user_prime_time.all()),
            len(user.user_activity.all()),
            len(user.user_prime_time.all())]))
    else:
        return []
