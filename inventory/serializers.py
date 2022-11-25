from rest_framework import serializers

from inventory import models


class InventoryModelSerializer(serializers.ModelSerializer):
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
