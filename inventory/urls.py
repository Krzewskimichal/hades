from django.urls import path, include
from rest_framework import routers

from inventory import views

urlpatterns = [
    path('projects', views.project_crud, name="inventory_crud"),
    path('projects/<str:pk>', views.project_crud, name="inventory_crud")
]
