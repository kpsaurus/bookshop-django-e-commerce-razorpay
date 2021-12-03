from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('get_full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'email', 'is_staff', 'is_active',)

    def get_full_name(self, obj):
        return obj.get_full_name()


admin.site.register(User, CustomUserAdmin)
