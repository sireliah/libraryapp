# -*- coding: utf-8 -*-

from rest_framework.test import APITestCase
from rest_framework import status

from bookapp.models import Book


class AuthTest(APITestCase):

    fixtures = [
        'bookapp/tests/fixtures/user.json',
    ]

    def test_authorization(self):
        response = self.client.post('/api/auth/',
                                    {'username': 'graves', 'password': 'exampleexample'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorization_negative(self):
        response = self.client.post('/api/auth/',
                                    {'username': 'graves', 'password': 'wrong'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookappTest(APITestCase):

    fixtures = [
        'bookapp/tests/fixtures/user.json',
        'bookapp/tests/fixtures/genre.json',
        'bookapp/tests/fixtures/book.json',
    ]

    def test_add_genre(self):
        self.client.login(username='graves', password='exampleexample')
        response = self.client.post('/api/genre/add/',
                                    {'name': 'science-fiction'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'name': 'science-fiction'})

    def test_add_genre_unauthenticated(self):
        response = self.client.post('/api/genre/add/',
                                    {'name': 'science-fiction'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_book(self):
        self.client.login(username='graves', password='exampleexample')
        response = self.client.post('/api/book/add/',
                                    {'title': 'I, Claudius',
                                     'genre': [1]},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'title': 'I, Claudius',
                                         'genre': [1, ]})

    def test_add_book_duplicate(self):
        self.client.login(username='graves', password='exampleexample')
        response = self.client.post('/api/book/add/',
                                    {'title': 'Claudius the God: And His Wife Messalina',
                                     'genre': [1]},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'title': ['Sorry, this book title already exists in your library.']})

    def test_add_book_limit(self):
        self.client.login(username='graves', password='exampleexample')

        # Create more books to exceed the limit
        for n in range(0, 6):
            Book.objects.create(title='example', author_id=2)

        response = self.client.post('/api/book/add/',
                                    {'title': 'Homers Daughter)',
                                     'genre': [1]},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': ['Sorry, you can have up to 5 books on the free account.']})

    def test_edit_book(self):
        self.client.login(username='graves', password='exampleexample')
        response = self.client.put('/api/book/1/edit/',
                                    {'title': 'Homers Daughter',
                                     'genre': [1]},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Homers Daughter',
                                         'genre': [1, ]})

    def test_edit_book_wrong_author(self):
        self.client.login(username='graves', password='exampleexample')
        response = self.client.put('/api/book/2/edit/',
                                    {'title': 'Caves of Steel',
                                     'genre': [1]},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': ['Sorry, you cannot edit a book that is not yours.']})