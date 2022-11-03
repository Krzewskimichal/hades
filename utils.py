import jwt
from django.conf import settings
from rest_framework.request import Request


#todo add secrets
CLIENT_ID = "260750330389-3l33066948vmlv0j40asketrnq0qt080.apps.googleusercontent.com"


def get_jwt_data(request: Request) -> dict:
    try:
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
        jwt_token = jwt_token.split(' ')[1]
    except AttributeError:
        return {}
    token_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
    return token_data
