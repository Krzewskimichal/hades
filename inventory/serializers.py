from django.contrib.auth.models import User
from rest_framework import serializers

from inventory import models


class InventoryModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = models.InventoryModel
        fields = '__all__'


class ProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectModel
        fields = '__all__'


class UserProjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProjectModel
        fields = '__all__'


class InventoryTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventoryTypeModel
        fields = '__all__'


class LocalizationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LocalizationModel
        fields = '__all__'


class InventoryStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventoryStatusModel
        fields = '__all__'


class UserProjectSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'date_joined')