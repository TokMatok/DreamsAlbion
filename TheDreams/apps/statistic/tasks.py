import threading
from typing import List

import requests

from logging import getLogger
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache

from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime

from .models import About
from Payments.models import Treasurer

logger = getLogger(__name__)


def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator


def update_user(user, data):
    pk_fame = data['KillFame']
    pve_fame = data['LifetimeStatistics']['PvE']['Total']
    gathering_fame = data['LifetimeStatistics']['Gathering']['All']['Total']
    craft_fame = data['LifetimeStatistics']['Crafting']['Total']
    all_fame = pk_fame + pve_fame + gathering_fame + craft_fame
    user.all_fame = all_fame
    user.pk_fame = pk_fame
    user.mob_fame = pve_fame
    user.gathering_fame = gathering_fame
    user.craft_fame = craft_fame

    user.save()


def get_response(api, param='') -> requests.get:
    return requests.get(f'https://gameinfo.albiononline.com/api/gameinfo/{api}/{settings.GUILD_ID}/{param}')


def collect_users_data():
    users = get_user_model()
    response = get_response('guilds', 'members')
    if response.ok:
        data = response.json()
        cache.set('fame_monitoring', {'data': data, 'last_update': datetime.now()})
        for u in data:
            user = users.objects.filter(username=u['Name'])
            if user:
                user = user[0]
                update_user(user, u)


def collect_about_data():
    response = get_response('guilds')
    if response.ok:
        data = response.json()
        cache.set('about_monitoring', {'data': data, 'last_update': datetime.now()})
        about = About.objects.filter(name=data['Name'])
        if about:
            about = about[0]
            about.alliance = data['AllianceTag']
            about.member_count = data['MemberCount']
            about.death_fame = data['DeathFame']
            about.kill_fame = data['killFame']
            about.guild_id = data['Id']
            about.alliance_id = data['AllianceId']
            about.save()


def fame_monitoring(fame_cache):
    if not fame_cache:
        logger.info('fame_monitoring. message={0}'.format('кеш фейма не найден.'))
        collect_users_data()
    else:
        if cache_timedelta_is_valid(fame_cache, {'minutes': 10}):
            logger.info('fame_monitoring. message={0}'.format('кеш фейма устарел.'))
            collect_users_data()


def about_monitoring(about_cache):
    if not about_cache:
        logger.info('about_monitoring. message={0}'.format('кеш информации о гильдии не найден.'))
        collect_about_data()
    else:
        if cache_timedelta_is_valid(about_cache, {'minutes': 10}):
            logger.info('about_monitoring. message={0}'.format('кеш информации о гильдии устарел.'))
            collect_about_data()


def cache_timedelta_is_valid(cache_element, delta) -> bool:
    if cache_element['last_update'] < datetime.now() - timedelta(**delta):
        return False
    else:
        return True


def treasurer_monitoring():
    treasurers: List[get_user_model] = get_user_model().objects.filter(groups__name="Казначей")
    for user in treasurers:
        if not Treasurer.objects.filter(treasurer_id=user.id):
            Treasurer.objects.create(treasurer_id=user.id)


@set_interval(10)
def pool_update():
    logger.info('fame_monitoring. message={0}'.format('Изьятие кэша'))
    fame_cache = cache.get('fame_monitoring')

    logger.info('about_monitoring. message={0}'.format('Изьятие кэша'))
    about_cache = cache.get('about_monitoring')

    # Проверка валидности и обновление
    fame_monitoring(fame_cache)
    about_monitoring(about_cache)
    treasurer_monitoring()
