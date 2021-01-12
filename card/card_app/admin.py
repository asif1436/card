from django.contrib import admin
from .models import Card, MyUser, OTP

# Register your models here.

admin.site.register(Card)

admin.site.register(MyUser)


class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "otp", "timestamp", "is_active")


admin.site.register(OTP, OTPAdmin)
