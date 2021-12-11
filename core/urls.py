from django.urls import path
from .views import index, logout, BookDetails, make_order

urlpatterns = [
    path('', index, name='index'),
    path('book/<pk>', BookDetails.as_view(), name='book-details'),
    path('make-order/', make_order, name='make-order'),
    path('logout', logout, name='sign-out')
]
