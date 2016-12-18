
from django.conf.urls import url
from django.contrib import admin

from bookapp.views import AddGenreView, AddBookView, UpdateBookView
from library.views import AuthView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/auth/', AuthView.as_view()),

    url(r'^api/genre/add/$', AddGenreView.as_view(), name='add_genre'),
    url(r'^api/book/add/$', AddBookView.as_view(), name='add_book'),
    url(r'^api/book/(?P<pk>\d+)/edit/$', UpdateBookView.as_view(), name='update_book')
]
