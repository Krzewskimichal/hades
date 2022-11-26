from django.urls import path, include
from rest_framework import routers

from inventory import views

urlpatterns = [
    path('projects', views.project_crud, name="inventory_crud"),
    path('projects/<str:pk>', views.project_crud, name="inventory_crud"),

    path('localization/<str:project_id>', views.localization_crud, name="localization_crud"),
    path('localization/<str:project_id>/<str:pk>', views.localization_crud, name="localization_crud"),

    path('inventory-status/<str:project_id>', views.inventory_status_crud, name="inventory_status_crud"),
    path('inventory-status/<str:project_id>/<str:pk>', views.inventory_status_crud, name="inventory_status_crud"),

    path('inventory-type/<str:project_id>', views.inventory_type_crud, name="inventory_type_crud"),
    path('inventory-type/<str:project_id>/<str:pk>', views.inventory_type_crud, name="inventory_type_crud"),

    path('inventory-item/<str:project_id>', views.inventory_crud, name="inventory_crud"),
    path('inventory-item/<str:project_id>/<str:pk>', views.inventory_crud, name="inventory_crud"),

    path('project_users/<str:project_id>', views.project_users, name="project_users"),
    path('project_users/<str:project_id>/<str:pk>', views.project_users, name="project_users")
]
