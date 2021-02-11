from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path('', include('statistic.urls')),
    path('ordering/', include('SRM.urls')),
    path('news/', include('Articles.urls')),
    path('payments/', include('Payments.urls')),
    path('grappelli/', include('grappelli.urls')),
    path("select2/", include("django_select2.urls")),
    path('fucking_admins/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
