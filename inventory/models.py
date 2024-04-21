import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class ProjectModel(models.Model):
    name = models.CharField(max_length=256)
    company_name = models.CharField(max_length=256)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProjectModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, null=True)

    class Role(models.TextChoices):
        OWNER = 'OW', 'Owner'
        ADMIN = 'AD', 'Admin'
        WAREHOUSEMAN = 'WA', 'Warehouseman'
        EMPLOYEE = 'EM', 'Employee'

    role = models.CharField(max_length=2, choices=Role.choices)

    def get_role(self) -> Role:
        return self.Role[self.role]

    class Meta:
        unique_together = ('user', 'project',)


class InventoryTypeModel(models.Model):
    name = models.CharField(max_length=256)
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class LocalizationModel(models.Model):
    place = models.CharField(max_length=256)
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.place


class InventoryStatusModel(models.Model):
    status = models.CharField(max_length=256)
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.status


class InventoryModel(models.Model):
    inventory_type = models.ForeignKey(InventoryTypeModel, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/', default=None, blank=True, null=True)
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256, blank=True)
    model = models.CharField(max_length=256, blank=True)
    localization = models.ForeignKey(LocalizationModel, on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=256, null=True)
    status = models.ForeignKey(InventoryStatusModel, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, null=True)
    qr_key = models.CharField(unique=True, max_length=512, null=True)
    custom_field = models.JSONField(max_length=2048, null=True)

    def __str__(self):
        return self.name


class InventoryHistoryModel(models.Model):
    inventory = models.ForeignKey(InventoryModel, on_delete=models.SET_NULL, null=True)
    what_happen = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    class ChangeType(models.TextChoices):
        OWNER = 'CO', 'change owner'
        ADMIN = 'CL', 'change localization'
        WAREHOUSEMAN = 'CS', 'change status'

    change_type = models.CharField(max_length=2, choices=ChangeType.choices)

    def get_role(self) -> ChangeType:
        return self.ChangeType[self.change_type]
