from django.urls import path
from .views import index, logout, BookDetails, make_order, gateway_response

urlpatterns = [
    path('', index, name='index'),
    path('book/<pk>', BookDetails.as_view(), name='book-details'),
    path('make-order/', make_order, name='make-order'),
    path('gateway-response', gateway_response, name='gateway-response'),
    path('logout', logout, name='sign-out')
]
