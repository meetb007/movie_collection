import uuid

from django.contrib.auth.models import User
from django.db import models

from movie.models import Movie


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=1000, null=True)
    movie = models.ManyToManyField(Movie, related_name="movie_collection",
                                   blank=True)
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='user_collection',
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'collection'
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
