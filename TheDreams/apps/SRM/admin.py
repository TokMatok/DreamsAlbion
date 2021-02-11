from django.contrib import admin

from django.contrib.auth import get_user_model

from .models import Order


class OrderTaskToInline(admin.TabularInline):
    model = Order.task_to.through
    extra = 1
    verbose_name = 'пользователь'
    verbose_name_plural = 'пользователю'


class OrderTaskToGroupInline(admin.TabularInline):
    model = Order.task_to_group.through
    extra = 1
    verbose_name = 'группа'
    verbose_name_plural = 'группе'


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderTaskToInline,
        OrderTaskToGroupInline
    ]
    exclude = ('task_to', 'task_to_group')
    list_display = ['task_from', 'get_users', 'get_groups', 'deathline', 'executed']


admin.site.register(Order, OrderAdmin)
