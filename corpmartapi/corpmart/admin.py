from django.contrib import admin

from .models import User, OneTimePassword, Business, Balancesheet, BalancesheetPayment, Blog, Testimonial, \
    ContactRequest
from django.apps import apps
from rest_framework.authtoken.models import Token


# De-register all models from other apps
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)


# admin.site.unregister(Token)


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)
admin.site.register(OneTimePassword)
admin.site.register(Business)
admin.site.register(Balancesheet)
admin.site.register(BalancesheetPayment)
admin.site.register(Blog)
admin.site.register(Testimonial)
admin.site.register(ContactRequest)
