import binascii
import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Category, BookType, Product, Order
from django.views.generic import DetailView, ListView
import os
from .forms import MakeOrderForm, PaymentGatewayResponse
import razorpay
import hmac
import hashlib
from django.contrib import messages


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

            if product.stock > 0:
                # Creating the Razorpay client object.
                client = razorpay.Client(auth=(os.getenv("RAZORPAY_ID"), os.getenv("RAZORPAY_SECRET_KEY")))

                # This is the data that needs to be passed onto Razorpay when creating an order.
                DATA = {
                    "amount": float(product.price * 100),
                    "currency": "INR",
                    "receipt": f"receipt for {product.book.title}",
                    "notes": {
                        "title": product.book.title,
                        "user": request.user.get_full_name()
                    }
                }
                # Creating a Razorpay order.
                resp = client.order.create(data=DATA)
                result = {'order_id': None}

                # If the order successfully created, return back the order id.
                if resp:
                    order_id = resp.get('id')
                    result = {'order_id': order_id}

                    # Creating an order.
                    Order.objects.create(
                        product=product,
                        user=request.user,
                        has_paid=False,
                        order_created_date=timezone.now(),
                        razorpay_order_id=order_id,
                        razorpay_payment_id=None,
                    )

                    # Updating the stock
                    product.stock = F('stock') - 1
                    product.save()

            else:
                result = {'status': 'Failed to purchase. Out of stock.'}
        else:
            result = form.errors

        return HttpResponse(json.dumps(result))
    else:
        return redirect('/')


@csrf_exempt
def gateway_response(request):
    form = PaymentGatewayResponse(request.POST)
    if form.is_valid():
        data = form.cleaned_data

        # Generating checksum for verification.
        message = data['razorpay_order_id'] + "|" + data['razorpay_payment_id']
        signature = hmac.new(bytes(os.getenv('RAZORPAY_SECRET_KEY'), 'latin-1'), bytes(message, 'latin-1'),
                             hashlib.sha256).hexdigest()

        # Checking the signature received from the gateway and generated signature same or not.
        if data['razorpay_signature'] == signature:
            # Signature match. Payment has been verified.
            # Updating the Order as payment successful.
            order_details = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
            order_details.razorpay_payment_id = data['razorpay_payment_id']
            order_details.has_paid = True
            order_details.save()
            messages.success(request, 'Payment has been successful. Order #ID: ' + str(order_details.pk))
            return redirect(reverse('index'))
        else:
            # Failed to verifiy the signature.
            messages.error(request, 'Failed to make the payment.')
            return redirect(reverse('index'))
    else:
        # Failed to get the proper response from the gateway.
        result = form.errors
    return redirect(reverse('index'))


@login_required
def user_orders(request):
    user = request.user
    user_orders_list = Order.objects.filter(user=user)
    categories = Category.objects.all()
    book_types = BookType.objects.all()
    return render(request, "core/user_orders.html", {
        'user_orders': user_orders_list,
        'categories': categories,
        'book_types': book_types
    })


def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))
