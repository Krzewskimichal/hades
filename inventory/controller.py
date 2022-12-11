from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User

from inventory.models import UserProjectModel
from utils import get_jwt_data


#todo
def check_permissions():
    pass


def check_token(request: Request):
    jwt_token_data = get_jwt_data(request)
    if not jwt_token_data:
        return Response({'error': 'missing access token'})
    return get_object_or_404(User, id=jwt_token_data.get('user_id'))


def check_role(project_id: str, user_id: str) -> str:
    """
        check role of logged user in project
    """
    user_project = UserProjectModel.objects.get(project_id=project_id, user_id=user_id)
    return user_project.role


def check_if_admin(project_id: str, user_id: str) -> bool:
    """
        check if logged user is owner or admin
    """
    role = check_role(project_id, user_id)
    return True if role in ('OW', 'AD') else False
