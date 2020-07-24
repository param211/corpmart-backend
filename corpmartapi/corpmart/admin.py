from django.contrib import admin

from .models import User, OneTimePassword, Business, Balancesheet, BalancesheetPayment, Blog, Testimonial, \
    ContactRequest


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
