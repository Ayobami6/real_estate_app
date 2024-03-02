from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/register', UserCreateAPIView.as_view()),
    path('api/login', LoginAPIView.as_view()),
]