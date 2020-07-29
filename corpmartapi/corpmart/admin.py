from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OneTimePassword, Business, Balancesheet, Blog, Testimonial, ContactRequest
from django.apps import apps
from rest_framework.authtoken.models import Token


# De-register all models from other apps
for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        if admin.site.is_registered(model):
            admin.site.unregister(model)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'mobile')
    list_filter = ('email', 'mobile',)
    fieldsets = (
        (None, {'fields': ('email', 'mobile', 'first_name', 'last_name', 'country_code', 'organisation_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)
        }
        ),
    )
    search_fields = ('email', 'mobile')
    ordering = ('email',)


# Register your models here.
class CustomBalancesheetAdmin(admin.ModelAdmin):
    list_display = ('business', 'uploaded_on',)
    ordering = ('uploaded_on',)


# class CustomBalancesheetPaymentAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'balancesheet', 'user', 'amount', 'date', 'order_id',
#                     'payment_successful')
#     ordering = ('date', 'transaction_id')
#     search_fields = ('transaction_id', 'order_id')
#     list_filter = ('user', 'balancesheet',)


class CustomBusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'business_name', 'posted_by', 'is_verified',)
    ordering = ('id', 'verified_by')
    list_filter = ('is_verified', 'state', 'industry', 'company_type', 'sub_type')
    search_fields = ('id', 'business_name', 'state', 'company_type', 'company_type_others_description', 'sub_type',
                     'sub_type_others_description', 'industry', 'industries_others_description', 'verified_by')


class CustomContactRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'requested_by', 'created_at', 'processed', 'processed_by', 'status')
    ordering = ('id', 'created_at')
    list_filter = ('processed', 'business', 'requested_by', 'created_at', 'processed_by')
    search_fields = ('id', 'business', 'requested_by', 'created_at', 'processed', 'processed_by', 'status')


admin.site.register(User, CustomUserAdmin)
# admin.site.register(OneTimePassword)
admin.site.register(Business, CustomBusinessAdmin)
admin.site.register(Balancesheet, CustomBalancesheetAdmin)
# admin.site.register(BalancesheetPayment, CustomBalancesheetPaymentAdmin)
admin.site.register(Blog)
admin.site.register(Testimonial)
admin.site.register(ContactRequest, CustomContactRequestAdmin)
