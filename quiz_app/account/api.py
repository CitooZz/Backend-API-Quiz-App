from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


from account.serializers import RegisterUserSerializer, CustomTokenObtainPairSerializer


class RegisterUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
