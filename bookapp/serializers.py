# -*- coding: utf-8 -*-

from rest_framework import serializers

from bookapp.models import Genre, Book


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', )


class CreateBookSerializer(serializers.ModelSerializer):

    """
    Called when using POST.
    """

    def validate(self, value):
        # Check the number of existing books of this user.
        books = Book.objects.filter(author_id=self.context['user'].id)
        if books.count() > 5:
            raise serializers.ValidationError({"error":"Sorry, you can have up to 5 books on the free account."})
        return value

    def validate_title(self, value):
        # Just check if the logged user has already book of this title.
        duplicated_books = Book.objects.filter(title=value,
                                               author_id=self.context['user'].id)
        if duplicated_books.exists():
            raise serializers.ValidationError("Sorry, this book title already exists in your library.")

        return value

    def create(self, validated_data):
        """
        We set the author based on the logged user.
        Also, we assign genre to the book instance.
        """
        validated_data['author'] = self.context['user']
        genre = validated_data.pop('genre', [])
        book = Book.objects.create(**validated_data)
        book.genre = genre
        book.save()
        return book

    class Meta:
        model = Book
        fields = ('title', 'genre', )


class UpdateBookSerializer(CreateBookSerializer):

    """
    This serializer (used for PUT requests) extends CreateBookSerializer
    with new functionality: checking whether author matches the logged user.
    """

    def validate(self, value):
        super(UpdateBookSerializer, self).validate(value)

        # User should be able to update only his own book.
        if self.instance.author != self.context['user']:
            raise serializers.ValidationError({"error":"Sorry, you cannot edit a book that is not yours."})

        return value

    def update(self, instance, validated_data):

        # Assign genres.
        instance.genre = validated_data.pop('genre', [])

        # Update the instance with new data.
        for field, attribute in validated_data.items():
            setattr(instance, field, attribute)

        instance.save()

        return instance

    class Meta:
        model = Book
        fields = ('title', 'genre', )
