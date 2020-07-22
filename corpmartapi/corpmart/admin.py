from django.contrib import admin

from .models import User, OneTimePassword


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)
admin.site.register(OneTimePassword)