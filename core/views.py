from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.urls import reverse
from .models import Book, Category, BookType, Product
from django.views.generic import DetailView


def index(request):
    category = request.GET.get('category')
    book_type = request.GET.get('book_type')
    categories = Category.objects.all()
    book_types = BookType.objects.all()
    if category is None:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(category__category=category).all()

    if book_type:
        books_as_per_book_type = Product.objects.filter(book_type__book_type=book_type).only('book')
        if books_as_per_book_type:
            books_as_per_book_type = [product.book.pk for product in books_as_per_book_type]
        else:
            books_as_per_book_type = []
        books_2 = Book.objects.filter(id__in=books_as_per_book_type)
        result_books = books.intersection(books_2)
    else:
        result_books = books

    return render(request, 'core/index.html', {
        'books': result_books,
        'categories': categories,
        'book_types': book_types
    })


class BookDetails(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()

        categories = Category.objects.all()
        book_types = BookType.objects.all()

        context['categories'] = categories
        context['book_types'] = book_types
        return context


def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))
