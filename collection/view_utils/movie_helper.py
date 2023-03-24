from collection.models import Collection


def fetch_movie_details(user, uuid):
    return Collection.objects.filter(user=user, id=uuid)\
        .first()\
        .movie\
        .values('title', 'description')
