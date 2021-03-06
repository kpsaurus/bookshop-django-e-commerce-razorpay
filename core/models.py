from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and _ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    display_name = models.CharField(max_length=100, null=True, blank=True,
                                    help_text='Alternate name')

    address = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'first_name', ]
    objects = UserManager()

    def __str__(self):
        if self.display_name:
            return self.display_name
        return self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        If the user has specified the display name, it will be returned.
        """
        if self.display_name:
            return self.display_name
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Category(models.Model):
    category = models.CharField(max_length=50, null=False, blank=False, help_text='Category of the book')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f'{self.category}'


class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    LANGUAGES = [
        ('ENGLISH', 'English'),
        ('FRENCH', 'French'),
        ('SPANISH', 'Spanish'),
    ]
    language = models.CharField(max_length=20, choices=LANGUAGES, blank=False, null=False)
    pages = models.IntegerField(null=False, blank=False)
    category = models.ManyToManyField(Category, related_name='book_categories')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_author')
    cover_image = models.ImageField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class BookType(models.Model):
    book_type = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f'{self.book_type}'


class Product(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_product')

    book_type = models.ForeignKey(BookType, null=True, on_delete=models.SET_NULL)
    price = models.FloatField(blank=False, null=False)
    stock = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return f'{self.book.title}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    has_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    order_created_date = models.DateTimeField(auto_created=True)
    order_updated_date = models.DateTimeField(auto_now=True)
    has_cancelled = models.BooleanField(default=False)
    cancelled_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.book.title} purchase from {self.user} on {self.order_created_date}'
