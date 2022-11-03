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
from django.shortcuts import get_list_or_404

from inventory.serializers import InventoryModelSerializer, ProjectModelSerializer, UserProjectModelSerializer
from inventory.models import InventoryModel, ProjectModel, UserProjectModel
from utils import get_jwt_data


@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
def inventory_crud(request: Request):
    pass


@api_view(['GET', 'POST', 'UPDATE', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_crud(request: Request, pk=None) -> Response:
    """
        CRUD for project model
    """
    jwt_token_data = get_jwt_data(request)
    if not jwt_token_data:
        return Response({'error': 'missing access token'})
    logged_user = get_object_or_404(User, id=jwt_token_data.get('user_id'))

    if request.method == 'GET':
        if pk:
            #todo more view
            project = get_object_or_404(ProjectModel, id=pk)
            serializer = ProjectModelSerializer(project)

        else:
            instance = [instance.project_id for instance in get_list_or_404(UserProjectModel, user_id=logged_user.id)]
            instance = ProjectModel.objects.filter(id__in=instance)
            # return Response(instance)
        # user_projects_ids = [user_project.id for user_project in user_projects]

            serializer = ProjectModelSerializer(instance, many=True)
            print(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            project = ProjectModel(name=request.POST.get('name'), company_name=request.POST.get('company_name'))
            project.save()
            user_project = UserProjectModel(user_id=int(logged_user.id), project=project, role='OW')
            user_project.save()
            return Response({'message': f"Project {project.name} created"}, status=status.HTTP_200_OK)
        except django.db.utils.IntegrityError:
            return Response({'message': 'missing requirement parameters'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

