import json

import requests
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import serializers
from .models import Attachment
from .permissions import IsOwnerOrAdminPermission

User = get_user_model()


class GoogleView(APIView):
    @extend_schema(
        request=serializers.GoogleTokenSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "description": "Refresh token"},
                    "access": {"type": "string", "description": "Access token"},
                },
            },
            400: {"type": "object", "description": "Validation errors or invalid token"},
        },
        description="Verify google token and activate the account.")
    def post(self, request):
        serializer = serializers.GoogleTokenSerializer(data=request.data)
        if serializer.is_valid():
            payload = {'access_token': serializer.data}
            r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
            data = json.loads(r.text)

            if 'error' in data:
                content = {'message': 'wrong google token / this google token is already expired.'}
                return Response(content)

            # create user if not exist
            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                user = User.objects.create_user(email=data['email'],
                                                first_name=data['first_name'],
                                                second_name=data['second_name'])

            token = RefreshToken.for_user(user)
            response = dict()
            response['first_name'] = user.first_name
            response['second_name'] = user.second_name
            response['access_token'] = str(token.access_token)
            response['refresh_token'] = str(token)
            return Response(response)
        return Response(serializer.errors, status=400)


class TokenView(TokenObtainPairView):
    pass


class RefreshView(TokenRefreshView):
    pass


class CreateAccountView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.AccountSerializer


class ManageAccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AccountSerializer
    def get_object(self):
        return self.request.user


class AvatarEditView(generics.UpdateAPIView):
    serializer_class = serializers.AvatarEditSerializer


    def get_object(self):
        return self.request.user


class AttachmentViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrAdminPermission, ]
    serializer_class = serializers.AttachmentSerializer

    def get_queryset(self):
        return Attachment.objects.filter(account=self.request.user).order_by("-created_at")
