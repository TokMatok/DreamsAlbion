from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from Payments.models import Payment, Treasurer


class TreasurerAdmin(admin.ModelAdmin):
    model = Treasurer
    list_display = ['treasurer']


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['date', 'whom', 'payment_amount', 'comment', 'confirm']


# class TreasurerAdmin(admin.ModelAdmin):
#     model = Treasurer
#     inlines = [PaymentsInline]
#     list_display = ['treasurer']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Treasurer, TreasurerAdmin)
