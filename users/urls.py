from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users import views


urlpatterns = [
    # path('', views.user_view),
    # path('<str:pk>', views.user_view),
    path('oauth', views.oauth, name='user_oath'),
    path('me', views.my_account, name='my_account'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
