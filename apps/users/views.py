import json

from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
import logging
import traceback
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class UserCreateAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if user:
                    token = Token.objects.create(user=user)
                    data = serializer.data
                    data['token'] = token.key
                    return JsonResponse(data, status=status.HTTP_201_CREATED)
                return JsonResponse({"error": _("Coudn\'t Create User")}, status=400)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            return JsonResponse({"error": "Something Went wrong!"}, status=500)

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Create or get a token for the user
            token = Token.objects.get(user=user)

            return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            return JsonResponse({"error": "Something Went wrong!"}, status=500)