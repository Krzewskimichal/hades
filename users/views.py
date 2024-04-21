import os
import rest_framework.request
from google.auth.transport import requests as google_requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from google.oauth2 import id_token
from collections.abc import Iterable
from django.http import JsonResponse
from django.core import serializers

# from utlis import get_jwt_data
from utils import get_jwt_data
from users.serializers import UserSerializer
from inventory.models import ProjectModel, UserProjectModel


@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def user_view(request, pk=None):
    if request.method == 'GET':
        instance = get_object_or_404(User, id=pk) if pk else User.objects.all()
        serializer = UserSerializer(instance, many=True) if isinstance(instance, Iterable) else UserSerializer(instance)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def oauth(request: rest_framework.request.Request) -> Response:
    if request.data.get('provider') == 'google':
        CLIENT_ID = os.getenv('GOOGLE_LOGIN_CLIENT_ID')
        token = request.data.get('id_token')
        try:
            token_data = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID, 100)
        except ValueError:
            return Response({'message': 'Invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'Unknown provider.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=token_data['email'])
    except User.DoesNotExist:
        user = User()
        user.username = token_data['email']
        user.password = make_password(BaseUserManager().make_random_password())
        user.email = token_data['email']
        try:
            user.first_name = token_data['given_name']
            user.last_name = token_data['family_name']
        except KeyError:
            print("Token doesn't contain given name or family name")
        user.save()

    refresh_token = RefreshToken.for_user(user)
    return Response({
        "email": user.email,
        "username": user.first_name,
        "access_token": str(refresh_token.access_token),
        "refresh_token": str(refresh_token)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_account(request: rest_framework.request.Request) -> JsonResponse:
    data = get_jwt_data(request)
    if not data:
        return JsonResponse({'error': 'missing access token'})
    user = get_object_or_404(User, id=data.get('user_id'))
    projects = UserProjectModel.objects.filter(user_id=user.id).select_related()
    projects_data = [{
        "id": project.project.id,
        "name": project.project.name,
        "role": project.role
    } for project in projects]
    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "username": user.first_name,
        "projects": projects_data
    })
