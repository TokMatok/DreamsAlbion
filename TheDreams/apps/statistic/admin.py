import threading

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import Activity, Recruit, UserActivity, About, PrimeTime, \
    UserPrimeTime, UserRole, Role, Mentor, Mentoring
from .tasks import pool_update


class UsersInLine(admin.TabularInline):
    model = get_user_model()
    extra = 1


class ActivitiesInline(admin.TabularInline):
    model = UserActivity.user_activity.through
    extra = 1
    verbose_name = 'активность'
    verbose_name_plural = 'активности'


class MentoringActivitiesInline(admin.TabularInline):
    model = Mentoring.direction_of_development.through
    extra = 1
    verbose_name = 'активность'
    verbose_name_plural = 'активности'


class PrimeTimeInline(admin.TabularInline):
    model = UserPrimeTime.user_prime_time.through
    extra = 1
    verbose_name = 'прайм-тайм'
    verbose_name_plural = 'прайм-таймы'


class UserRoleInline(admin.TabularInline):
    model = UserRole.user_role.through
    extra = 1
    verbose_name = 'роль'
    verbose_name_plural = 'роли'


class MentoringInline(admin.TabularInline):
    model = Mentoring.people.through
    extra = 1
    verbose_name = 'сопровождаемый'
    verbose_name_plural = 'сопровождаемые'


class RecruitInline(admin.TabularInline):
    model = Recruit.invitee.through
    extra = 1
    verbose_name = 'рекрут'
    verbose_name_plural = 'рекруты'


class RoleAdmin(ModelAdmin):
    inlines = [
        UserRoleInline,
    ]
    exclude = ('user_role',)
    list_display = ['role_name', 'get_users']


class RecruitAdmin(ModelAdmin):
    inlines = [
        RecruitInline,
    ]
    exclude = ('invitee',)
    list_display = ['recruiter', 'user_fame', 'week']


class UserActivityAdmin(ModelAdmin):
    inlines = [
        ActivitiesInline,
    ]
    exclude = ('user_activity',)
    list_display = ['activity', 'get_users']


class PrimeTimeAdmin(ModelAdmin):
    inlines = [
        PrimeTimeInline,
    ]
    exclude = ('users',)
    list_display = ['prime_time', 'get_users']


class MentoringAdmin(admin.ModelAdmin):
    inlines = [
        MentoringInline,
        MentoringActivitiesInline
    ]
    exclude = ('people', 'direction_of_development')
    list_display = ['mentor', 'get_users']


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = get_user_model()
    list_display = ['username', 'timezone', 'all_fame',
                    'phone', 'city',
                    'user_activity_get_names', 'user_prime_time_names']
    inlines = [ActivitiesInline,
               PrimeTimeInline,
               UserRoleInline,
               # PaymentInline,
               ]

    fieldsets = UserAdmin.fieldsets + (
        ('Персональная информация', {'fields': ('city', 'phone', 'timezone')}),
        ('Приватность', {'fields': ('phone_hidden', 'email_hidden')}),
        (None, {'fields': ('code', 'join_date')}),
        ('Фейм', {'fields': ('all_fame', 'pk_fame', 'mob_fame', 'gathering_fame', 'craft_fame')}),
    )


CustomUserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'timezone', 'password1', 'password2',)}
     ),
)

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Recruit, RecruitAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(UserPrimeTime, PrimeTimeAdmin)
admin.site.register(UserRole, RoleAdmin)
admin.site.register(Mentoring, MentoringAdmin)

admin.site.register(Mentor)
admin.site.register(PrimeTime)
admin.site.register(Activity)
admin.site.register(Role)
admin.site.register(About)

threading.Thread(target=pool_update).start()
