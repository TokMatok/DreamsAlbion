from django.shortcuts import render, redirect
from .models import Order
from itertools import chain


# Create your views here.
def index(request):
    if request.user.is_staff:
        orders_for_me = Order.objects.filter(task_to=request.user)
        orders_for_my_group = Order.objects.filter(task_to_group__in=request.user.groups.all())
        groups_names = set(orders_for_my_group.values_list('task_to_group__name', flat=True))
        deathline = Order.objects.filter(
            task_to_group__in=request.user.groups.all(), executed=False).order_by(
            'deathline') | Order.objects.filter(
            task_to=request.user, executed=False).order_by('deathline')
        last_5_for_me = orders_for_me.order_by('-post_date')[:5]
        return render(request, 'SRM/index.html',
                      context={"page_title": 'Задачи',
                               'orders_for_me': orders_for_me.order_by('-post_date'),
                               'orders_for_my_group': orders_for_my_group.order_by('-post_date'),
                               'last_5_for_me': last_5_for_me,
                               'deathline': deathline,
                               'groups_names': groups_names
                               })
    else:
        redirect('/')


def view_order(request, order_id):
    if request.user.is_staff:
        order = Order.objects.filter(id=order_id)
        if order:
            order = order[0]

        return render(request, 'SRM/order.html',
                      context={"page_title": 'Задача не найдена' if not order else f'Задача - {order.topic}',
                               'order': order,
                               })
    else:
        redirect('/')
