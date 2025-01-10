from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.db import transaction
from django.db.models import F

class BookPagination(PageNumberPagination):
    page_size = 5


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        book = self.get_object()
        if book.count > 0:
            book.count = F('count') - 1
            book.save()
            return Response({"message": "Книга успешно куплена"})
        return Response({"error": "Книги нет в наличии"}, status=status.HTTP_400_BAD_REQUEST)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer