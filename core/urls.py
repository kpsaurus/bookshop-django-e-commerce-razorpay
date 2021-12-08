from django.urls import path
from .views import index, logout, search_books

urlpatterns = [
    path('', index, name='index'),
    path('search', search_books, name='search-books'),
    path('logout', logout, name='sign-out')
]
