from django.contrib import admin

# Register your models here.
from .models import Plan, Subscription, ExchangeRateLog, Wallet

admin.site.register(ExchangeRateLog)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Wallet)