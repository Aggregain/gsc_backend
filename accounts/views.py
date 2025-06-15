import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers, tasks
from .models import Attachment, Account

User = get_user_model()


class GoogleView(APIView):
    permission_classes = (AllowAny,)
    @extend_schema(
        request=serializers.GoogleTokenSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "description": "Refresh token"},
                    "access": {"type": "string", "description": "Access token"},
                    "is_staff": {"type": "boolean", "description": "Is staff"},
                },
            },
            400: {"type": "object", "description": "Validation errors or invalid token"},
        },
        description="Verify google token and activate the account.")
    def post(self, request):
        serializer = serializers.GoogleTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_SECRET_KEY,
            'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
            'grant_type': 'authorization_code',
        }
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        data = r.json()

        if 'error' in data:
            content = {'message': data}
            return Response(content)

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(email=data['email'],
                                            first_name=data['given_name'],
                                            second_name=data['family_name'],
                                            is_active=True,)

        token = RefreshToken.for_user(user)
        response = dict()

        response['access'] = str(token.access_token)
        response['refresh'] = str(token)
        response['is_staff'] = user.is_staff
        return Response(data=response, status=200)


class TokenView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer



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


class AccountDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.AccountDetailSerializer

    def get_queryset(self):
        return Account.objects.prefetch_related('attachments').all()

    def get_object(self):
        account =super().get_object()
        if not self.request.user.is_staff or not self.request.user == account:
            raise PermissionDenied
        return account

class AttachmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.AttachmentSerializer

    def get_queryset(self):
        user = self.request.user
        return Attachment.objects.filter( Q(account=user) | Q(application__owner=user)).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class ConfirmEmailSendView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=serializers.EmailConfirmSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "description": "success message"},
                },
            },
            400: {"type": "object", "description": "Validation errors"},
        },
        description="Verify google token and activate the account.")
    def post(self, request, *args, **kwargs):
        serializer = serializers.EmailConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'detail': f"Ссылка на подтверждение аккаунта отправлена на почту {serializer.validated_data['email']}"},
                        status=status.HTTP_200_OK)



class EmailConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"detail": "Недействительная ссылка"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(settings.FRONTEND_BASE_URL)
        return Response({"detail": "Недействительная ссылка"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=serializers.PasswordResetSerializer,
        description="reset password",)
    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Письмо со ссылкой для сброса пароля отправлено на ваш email"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=serializers.PasswordResetConfirmSerializer,
        description="Confirm password reset.")
    def post(self, request):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'detail': 'Пароль успешно изменен'},status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
