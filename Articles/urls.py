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
    path('', views.articles, name='article'),
    path('faq', views.faq, name='faq'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
