from django.contrib import admin

# Register your models here.
from Articles.models import New, FAQ

admin.site.register(New)
admin.site.register(FAQ)

