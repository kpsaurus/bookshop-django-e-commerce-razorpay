import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.urls import reverse
from .models import Book, Category, BookType, Product
from django.views.generic import DetailView
import os
from .forms import MakeOrderForm
import razorpay


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

        object = kwargs.get('object')

        book_products = object.book_product.all()

        categories = Category.objects.all()
        book_types = BookType.objects.all()

        context['categories'] = categories
        context['book_types'] = book_types
        context['book_products'] = book_products
        return context


@login_required
def make_order(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)

        form = MakeOrderForm(data)

        if form.is_valid():
            selected_product = form.cleaned_data['selected_product']
            product = Product.objects.get(pk=selected_product)
            # Creating the Razorpay client object.
            client = razorpay.Client(auth=(os.getenv("RAZORPAY_ID"), os.getenv("RAZORPAY_SECRET_KEY")))

            # This is the data that needs to be passed onto Razorpay when creating an order.
            DATA = {
                "amount": float(product.price * 100),
                "currency": "INR",
                "receipt": f"receipt for {product.book.title}",
                "notes": {
                    "title": product.book.title,
                    "user": request.user
                }
            }
            # Creating a Razorpay order.
            resp = client.order.create(data=DATA)
            result = {'order_id': None}

            # If the order successfully created, return back the order id.
            if resp:
                order_id = resp.get('id')
                result = {'order_id': order_id}
        else:
            result = form.errors

        return HttpResponse(json.dumps(result))
    else:
        return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))
