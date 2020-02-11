from rest_framework import viewsets
from permissions.permissions import IsAdminOrReadCreate

from book_shop.models import Author, Book, Order, Publisher
from book_shop.serializer import (
    AuthorSerializer,
    BookSerializer,
    OrderSerializer,
    PublisherSerializer,
)


class AuthorView(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class PublisherView(viewsets.ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()


class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAdminOrReadCreate]
