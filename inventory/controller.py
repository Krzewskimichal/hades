import django.db.utils
import smtplib
import ssl
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User

from inventory.models import UserProjectModel, InventoryHistoryModel, InventoryModel
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


def check_if_warehouseman(project_id: str, user_id: str) -> bool:
    """
        check if logged user is owner or admin
    """
    role = check_role(project_id, user_id)
    return True if role in ('OW', 'AD', 'WA') else False


def send_email(message: str, receiver: str):
    """
        send email
    """

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "hades.project.qr@gmail.com"
    receiver_email = receiver
    password = "HadesQR345"
    message = message
    # message = """\
    # Subject: Hi there
    #
    # This message is sent from Python."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def add_inventory_to_history(request, pk):
    """
        pass
    """
    possibles = {
        'CO': request.data.get('employee')
        # 'CL': request.data.get('localization'),
        # 'CS': request.data.get('status')
    }
    full_phrases = {
        'CO': 'change employee from {} to {}'
        # 'CL': 'change localization from {} to {}',
        # 'CS': 'change status from {} to {}'
    }
    for key, value in possibles.items():
        try:
            if value:
                inventory = InventoryModel.objects.filter(id=pk).select_related()[0]
                user = User.objects.get(id=value)
                user_username = user.username if user.username else "no one"
                inventory_username = inventory.employee.username if inventory.employee else "no one"
                if user_username != inventory_username:
                    message = full_phrases[key].format(inventory_username, user_username)
                    inventory_history = InventoryHistoryModel(inventory_id=pk, what_happen=message, change_type=key)
                    inventory_history.save()
            return True
        except django.db.utils.IntegrityError:
            return False


def decode_image_base64(image: str):
    format, imgstr = image.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data
