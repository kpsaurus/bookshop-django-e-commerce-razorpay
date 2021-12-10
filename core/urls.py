from django.urls import path
from .views import index, logout, BookDetails

urlpatterns = [
    path('', index, name='index'),
    path('book/<pk>', BookDetails.as_view(), name='book-details'),
    path('logout', logout, name='sign-out')
]
