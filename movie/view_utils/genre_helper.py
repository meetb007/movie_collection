from movie.models import Genre


def bulk_create_genres(genre_name_list):
    genre_obj_list = Genre.objects \
        .filter(name__in=genre_name_list)

    existing_genre_name_list = genre_obj_list \
        .values_list('name', flat=True)

    genre_list = [
        Genre(name=genre_name)
        for genre_name in genre_name_list
        if genre_name not in existing_genre_name_list
    ]

    new_genre_obj_list = Genre.objects.bulk_create(genre_list)
    list(genre_obj_list).extend(new_genre_obj_list)

    return genre_obj_list
