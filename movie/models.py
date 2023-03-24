import uuid

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True,
                            unique=True, db_index=True)

    class Meta:
        db_table = 'genre'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=1000, null=True)
    genre = models.ManyToManyField(Genre, related_name='genre_movie',
                                   blank=True)

    class Meta:
        db_table = 'movie'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
