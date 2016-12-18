# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return "%s" % self.name


class Book(models.Model):

    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return "%s: %s" % (self.author.username, self.title)