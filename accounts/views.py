import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import serializers
from .client import GoogleOAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = GoogleOAuth2Client


class GoogleLoginCallback(APIView):

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = request.build_absolute_uri(reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=status.HTTP_200_OK)


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_CLIENT_ID,
            },
        )


class TokenView(TokenObtainPairView):
    pass


class RefreshView(TokenRefreshView):
    pass


class CreateAccountView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.CreateAccountSerializer


class ManageAccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CreateAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
