from .models import User, Category, Book, Author, Product, BookType
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


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
    pass
