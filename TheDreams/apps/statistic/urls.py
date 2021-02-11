from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

app_name = 'statistic'

handler400 = 'statistic.views.bad_request'
handler403 = 'statistic.views.permission_denied'
handler404 = 'statistic.views.page_not_found'
handler500 = 'statistic.views.server_error'

urlpatterns = [
    path('', views.index, name='index'),
    path("select2/", include("django_select2.urls")),

    # Контент
    path('top', views.top, name='top'),
    path('organisation/<str:organisation_name>', views.organisation, name='organisation'),
    # Админка
    path('required_add', views.required_add, name='required_add'),
    path('required_admin', views.required_admin, name='required_admin'),

    # Авторизация
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),

    # Аккаунт
    path("register", views.register, name="register"),
    path('activation_code_form', views.end_reg, name="end_reg"),
    path('change_user', views.change_user, name='change_user'),
    path('mail', views.mail_template, name="mail"),

    # path('change-password',
    #      auth_views.PasswordChangeView.as_view(template_name='change-password.html', success_url='/'),
    #      name='change_password'),

    # path('threads', views.threads_list, name='threads'),
    path('account/<str:user_name>', views.profile, name='profile'),
    path('groups/<str:group_name>', views.group, name='group'),
    path('account/', views.user_profile, name='profile'),

    # path('<int:thread_id>/leave_comment/', views.leave_comment, name='leave_comment'),

]

# handler404 = views.error_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
