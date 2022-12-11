import base64
import django.db.utils
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from collections.abc import Iterable
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.core import serializers

from users.serializers import UserSerializer
from inventory.serializers import InventoryModelSerializer, ProjectModelSerializer, UserProjectModelSerializer,\
    LocalizationModelSerializer, InventoryStatusModelSerializer, InventoryTypeModelSerializer
from inventory.models import InventoryModel, ProjectModel, UserProjectModel, LocalizationModel, InventoryStatusModel,\
    InventoryTypeModel, InventoryHistoryModel
from utils import get_jwt_data
from inventory.controller import check_token, check_if_admin, add_inventory_to_history, decode_image_base64


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_crud(request: Request, pk=None) -> JsonResponse:
    """
        CRUD for project model
    """
    logged_user = check_token(request)
    is_admin = False
    if pk:
        is_admin = check_if_admin(project_id=pk, user_id=logged_user.id)

    if request.method == 'GET':
        data = {}
        if pk:
            project = get_object_or_404(ProjectModel, id=pk)
            serializer = ProjectModelSerializer(project)
            data.update(serializer.data)
            user_project = UserProjectModel.objects.filter(project_id=pk).select_related()
            user_project_data = [{
                "id": user.user.id,
                "username": user.user.username,
                "email": user.user.email,
                "role": user.role
            } for user in user_project]
            data["users"] = user_project_data
        else:
            instance = [instance.project_id for instance in get_list_or_404(UserProjectModel, user_id=logged_user.id)]
            instance = ProjectModel.objects.filter(id__in=instance)
            serializer = ProjectModelSerializer(instance, many=True)
            data.update({"projects": serializer.data})
        return JsonResponse(data)
    elif request.method == 'POST':
        try:
            project = ProjectModel(name=request.data.get('name'), company_name=request.data.get('company_name'))
            project.save()
            user_project = UserProjectModel(user_id=int(logged_user.id), project=project, role='OW')
            user_project.save()
            return JsonResponse({'message': f"Project {project.name} created"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return JsonResponse({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        if pk and is_admin:
            project = get_object_or_404(ProjectModel, id=pk)
            serializer = ProjectModelSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': f"Project {project.name} updated"}, status=status.HTTP_200_OK)
            return JsonResponse({'message': f"Cannot update {project.name} project, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'message': f"Missing project id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk and is_admin:
            project = get_object_or_404(ProjectModel, id=pk)
            project.delete()
            return JsonResponse({'message': f"Project {project.name} has been deleted"}, status=status.HTTP_200_OK)
        return JsonResponse({'message': f"Missing project id!"}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def localization_crud(request: Request, project_id=None, pk=None) -> Response:
    """
        crud for localization available in project
    """

    logged_user = check_token(request)
    if request.method == 'GET':
        if pk:
            localization = get_object_or_404(LocalizationModel, id=pk)
            serializer = ProjectModelSerializer(localization)
        else:
            instance = LocalizationModel.objects.filter(project_id=project_id)
            serializer = LocalizationModelSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            project = get_object_or_404(ProjectModel, id=project_id)
            localization = LocalizationModel(project_id=project.id, place=request.data.get('place'))
            localization.save()
            return Response({'message': f"Localization: {localization.place} add to {project.name} project"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        if pk:
            localization = get_object_or_404(LocalizationModel, id=pk)
            serializer = LocalizationModelSerializer(localization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': f"Localization {localization.place} updated"}, status=status.HTTP_200_OK)
            return Response({'message': f"Cannot update {localization.place} localization, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"Missing localization id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk:
            localization = get_object_or_404(LocalizationModel, id=pk)
            localization.delete()
            return Response({'message': f"Localization {localization.place} has been deleted"}, status=status.HTTP_200_OK)
        return Response({'message': f"Missing Localization id!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def inventory_status_crud(request: Request, project_id=None, pk=None) -> Response:
    """
        crud for inventory status available in project
    """

    logged_user = check_token(request)
    if request.method == 'GET':
        if pk:
            inventory_status = get_object_or_404(InventoryStatusModel, id=pk)
            serializer = InventoryStatusModelSerializer(inventory_status)
        else:
            inventory_status = InventoryStatusModel.objects.filter(project_id=project_id)
            serializer = InventoryStatusModelSerializer(inventory_status, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            project = get_object_or_404(ProjectModel, id=project_id)
            inventory_status = InventoryStatusModel(project_id=project.id, status=request.data.get('status'))
            inventory_status.save()
            return Response({'message': f"Status: {inventory_status.status} add to {project.name} project"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        if pk:
            inventory_status = get_object_or_404(InventoryStatusModel, id=pk)
            serializer = InventoryStatusModelSerializer(inventory_status, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': f"status {inventory_status.status} updated"}, status=status.HTTP_200_OK)
            return Response({'message': f"Cannot update {inventory_status.status} status, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"Missing status id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk:
            inventory_status = get_object_or_404(InventoryStatusModel, id=pk)
            inventory_status.delete()
            return Response({'message': f"status {inventory_status.status} has been deleted"}, status=status.HTTP_200_OK)
        return Response({'message': f"Missing status id!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def inventory_type_crud(request: Request, project_id=None, pk=None) -> Response:
    """
        crud for inventory status available in project
    """

    logged_user = check_token(request)
    if request.method == 'GET':
        if pk:
            inventory_type = get_object_or_404(InventoryTypeModel, id=pk)
            serializer = InventoryTypeModelSerializer(inventory_type)
        else:
            inventory_type = InventoryTypeModel.objects.filter(project_id=project_id)
            serializer = InventoryTypeModelSerializer(inventory_type, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            project = get_object_or_404(ProjectModel, id=project_id)
            inventory_type = InventoryTypeModel(project_id=project.id, name=request.data.get('name'))
            inventory_type.save()
            return Response({'message': f"Type: {inventory_type.name} add to {project.name} project"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        if pk:
            inventory_type = get_object_or_404(InventoryTypeModel, id=pk)
            serializer = InventoryTypeModelSerializer(inventory_type, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': f"type {inventory_type.name} updated"}, status=status.HTTP_200_OK)
            return Response({'message': f"Cannot update {inventory_type.name} type, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"Missing type id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk:
            inventory_type = get_object_or_404(InventoryTypeModel, id=pk)
            inventory_type.delete()
            return Response({'message': f"type {inventory_type.name} has been deleted"}, status=status.HTTP_200_OK)
        return Response({'message': f"Missing type id!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def inventory_crud(request: Request, project_id=None, pk=None):
    """
        crud for inventory item available in project
    """

    logged_user = check_token(request)
    if request.method == 'GET':
        data = {}
        if pk:
            inventory = get_object_or_404(InventoryModel, id=pk)
            serializer = InventoryModelSerializer(inventory)
            data.update(serializer.data)
            history = InventoryHistoryModel.objects.filter(inventory_id=pk)
            history_data = [{
                "item": hist.inventory.id,
                "change": hist.what_happen,
                "date": hist.date
            } for hist in history]
            data['history'] = history_data
        else:
            inventory = InventoryModel.objects.filter(project_id=project_id)
            serializer = InventoryModelSerializer(inventory, many=True)
            data.update({"items": serializer.data})
        return JsonResponse(data)
    elif request.method == 'POST':
        try:
            project = get_object_or_404(ProjectModel, id=project_id)
            inventory_item = InventoryModel(project_id=project.id, name=request.data.get('name'))
            serializer = InventoryModelSerializer(inventory_item, data=request.data)
            # if request.data.get('image'):
            #     request.data['image'] = decode_image_base64(request.data.get('image'))
            if serializer.is_valid():
                serializer.save()
            return Response({'message': f"Inventory item: {inventory_item.name} add to {project.name} project"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        if pk:
            inventory_item = get_object_or_404(InventoryModel, id=pk)
            # if request.data.get('image'):
            #     request.data['image'] = decode_image_base64(request.data.get('image'))
            add_inventory_to_history(request, pk)
            serializer = InventoryModelSerializer(inventory_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': f"Item {inventory_item.name} updated"}, status=status.HTTP_200_OK)
            return Response({'message': f"Cannot update {inventory_item.name} item, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': f"Missing item id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if pk:
            inventory_item = get_object_or_404(InventoryModel, id=pk)
            inventory_item.delete()
            return Response({'message': f"type {inventory_item.name} has been deleted"}, status=status.HTTP_200_OK)
        return Response({'message': f"Missing type id!"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_users(request: Request, project_id=None, pk=None) -> Response:
    """
        crud for managing users in project
    """

    logged_user = check_token(request)
    if request.method == 'GET':
        if pk:
            user = get_object_or_404(User, id=pk)
            serializer = UserSerializer(user)
        else:
            user_ids = [user.user_id for user in UserProjectModel.objects.filter(project_id=project_id)]
            users = get_list_or_404(User, id__in=user_ids)
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.data.get('email'):
            return Response({'message': 'missing user email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_object_or_404(User, email=request.data.get('email'))
            if UserProjectModel.objects.get(user_id=user.id, project_id=project_id):
                return Response({'message': f"User {user.username} is already assign to project"}, status=status.HTTP_200_OK)
            user_project = UserProjectModel(project_id=project_id, user_id=user.id, role=request.data.get('role'))
            user_project.save()
            return Response({'message': f"Add user to project"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'PATCH':
    #     if pk:
    #         user_project = get_object_or_404(UserProjectModel, id=pk)
    #         serializer = InventoryModelSerializer(inventory_item, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'message': f"Item {inventory_item.name} updated"}, status=status.HTTP_200_OK)
    #         return Response({'message': f"Cannot update {inventory_item.name} item, data invalid"}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'message': f"Missing item id!"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user = get_object_or_404(User, email=request.GET.get('id'))
        user_project = get_object_or_404(UserProjectModel, project_id=project_id, user_id=user.id)
        user_project.delete()
        return Response({'message': f"User has been removed from project"}, status=status.HTTP_200_OK)
    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)