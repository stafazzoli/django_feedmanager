from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreateAPIView

app_name = 'accounts'

urlpatterns = [
    path('v1/register/', UserCreateAPIView.as_view(), name='register'),
    path('v1/login/', obtain_auth_token, name='login'),
]
