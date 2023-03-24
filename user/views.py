import logging
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.forms.user_forms import UserForm
from user.view_utils.jwt_helper import get_tokens_for_user

logger = logging.getLogger('django')


@api_view(['POST'])
def create_user(request):
    try:
        user_form = UserForm(request.data)

        if not user_form.is_valid():
            return Response(
                data={
                    'message': user_form.errors
                },
                status=400
            )

        user_data = user_form.cleaned_data
        user = User.objects.create(**user_data)

        return Response(data=get_tokens_for_user(user), status=201)

    except Exception as e:
        logger.exception(e)
        return Response(
            data={
                'message': 'Something went wrong',
                'exception': str(e)
            },
            status=500
        )


@api_view(['POST'])
def login_user(request):
    try:
        user_form = UserForm(request.data)

        if not user_form.is_valid():
            return Response(
                data={
                    'message': user_form.errors
                },
                status=400
            )

        user_data = user_form.cleaned_data
        user = User.objects.get(**user_data)

        return Response(data=get_tokens_for_user(user), status=200)

    except Exception as e:
        return Response(
            data={
                'message': 'Something went wrong',
                'exception': str(e)
            },
            status=500
        )
