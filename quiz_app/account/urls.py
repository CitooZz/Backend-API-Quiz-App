from django.urls import path

from account.api import RegisterUserView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view())
]
