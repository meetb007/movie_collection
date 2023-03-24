from django.contrib.auth.models import User
from rest_framework.response import Response


def validate_user(request):
    is_valid_user = True
    response = None
    username = request.user.username
    password = request.user.password
    user = User.objects \
        .filter(username=username, password=password) \
        .first()

    if not user:
        is_valid_user = False
        response = Response(
            data={
                'message': 'Invalid username or password'
            },
            status=400
        )

    return is_valid_user, response, user
