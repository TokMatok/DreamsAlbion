from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

app_name = 'articles'

handler400 = 'statistic.views.bad_request'
handler403 = 'statistic.views.permission_denied'
handler404 = 'statistic.views.page_not_found'
handler500 = 'statistic.views.server_error'

urlpatterns = [
    path('', views.index, name='payments'),
    path("get_debt", views.get_debt, name='get_debt'),
    path("get_payments_for_user", views.get_payments_for_user,
         name='get_payments_for_user'),
    path("set_payment_state", views.set_payment_state, name='set_payment_state'),
    path("get_sum_payments_not_confirm", views.get_sum_payments_not_confirm, name='get_sum_payments_not_confirm'),
    path("get_sum_payments_confirm", views.get_sum_payments_confirm, name='get_sum_payments_confirm'),
    path("add_payment/", views.add_payment, name='add_payment'),
    path("select2/", include("django_select2.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
