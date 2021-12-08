from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.urls import reverse
from .models import Book, Category, BookType


def index(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    book_types = BookType.objects.all()
    return render(request, 'core/index.html', {
        'books': books,
        'categories': categories,
        'book_types': book_types
    })


def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))


def search_books(request):
    category = request.GET['category']
    if category is None:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(category__category=category).all()
    return render(request, 'core/books.html', {
        'books': books,
    })
