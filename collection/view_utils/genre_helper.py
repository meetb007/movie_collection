from django.db.models import Count

from collection.models import Collection


def fetch_favourite_genres(user):
    genre_list = Collection.objects\
                     .filter(user=user)\
                     .values('movie__genre__name')\
                     .annotate(count=Count('movie__genre__name'))\
                     .order_by('-count')\
                     .values_list('movie__genre__name', flat=True)[:3]

    return ','.join(genre_list)

