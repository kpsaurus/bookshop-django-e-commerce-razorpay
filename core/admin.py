from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category
from django.contrib import admin


# Register your models here.
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'email', 'is_staff', 'is_active',)

    def get_full_name(self, obj):
        return obj.get_full_name()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass