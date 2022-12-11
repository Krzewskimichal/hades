from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User

from utils import get_jwt_data


#todo
def check_permissions():
    pass


def check_token(request: Request):
    jwt_token_data = get_jwt_data(request)
    if not jwt_token_data:
        return Response({'error': 'missing access token'})
    return get_object_or_404(User, id=jwt_token_data.get('user_id'))


def check_if_admin(role: str) -> bool:
    """
        check if logged user is owner or admin
    """
    return True if role in ('OW', 'AD') else False
