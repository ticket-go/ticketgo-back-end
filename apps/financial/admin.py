from django.contrib import admin

from apps.financial.models import Payment, Purchase

# Register your models here.
admin.site.register(Purchase)
admin.site.register(Payment)
