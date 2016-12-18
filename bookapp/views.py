# -*- coding: utf-8 -*-

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions

from bookapp.serializers import GenreSerializer, CreateBookSerializer, UpdateBookSerializer
from bookapp.models import Book


class AddGenreView(CreateAPIView):

    """
    Adds new genre.
    """

    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return super(AddGenreView, self).post(request, *args, **kwargs)


class AddBookView(CreateAPIView):

    """
    Adds new book.
    """

    serializer_class = CreateBookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        # Pass the user instance to the serializer context.
        return {'user': self.request.user}

    def post(self, request, *args, **kwargs):
        return super(AddBookView, self).post(request, *args, **kwargs)


class UpdateBookView(UpdateAPIView):

    """
    Replaces the chosen book with new data.
    """

    queryset = Book.objects.all()
    serializer_class = UpdateBookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        return {'user': self.request.user}

    def put(self, request, *args, **kwargs):
        return super(UpdateBookView, self).put(request, *args, **kwargs)
