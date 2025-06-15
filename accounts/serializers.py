from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import tasks
from .models import Attachment
from .utils import adjust_phone_number
from .validators import validate_phone_number


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_staff'] = self.user.is_staff
        return data

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = ['account', ]
        read_only_fields = ['id', ]


class AccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    phone_number = serializers.CharField(max_length=19,
                                         validators=[validate_phone_number],
                                         required=False)

    class Meta:
        model = get_user_model()

        fields = ['first_name', 'second_name', 'last_name', 'email', 'avatar',
                  'degree', 'gre_grade', 'gmat_grade', 'duolingo_grade', 'sat_grade',
                  'toefl_grade', 'toefl_grade', 'ielts_grade', 'gpa_grade',
                  'education_place', 'country', 'city', 'birth_date', 'phone_number', 'password']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True,

                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        if validated_data.get('phone_number'):
            adjusted_number = adjust_phone_number(validated_data['phone_number'])
            validated_data['phone_number'] = adjusted_number
        try:
            user = get_user_model().objects.get(email=validated_data['email'])
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(**validated_data)
        tasks.send_confirmation_email.delay(user.email_confirmation_url, user.email)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AccountDetailSerializer(AccountSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['attachments']


class AvatarEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar', ]


class GoogleTokenSerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = get_user_model().objects.get(email=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")
        return value

    def save(self):
        tasks.send_password_reset_email.delay(self.user.password_reset_url,
                                              self.user.email, )


class EmailConfirmSerializer(PasswordResetSerializer):
    def save(self):
        tasks.send_confirmation_email.delay(self.user.email_confirmation_url,
                                            self.user.email)

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uidb64'])
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise serializers.ValidationError("Недействительная ссылка для сброса пароля")

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError("Недействительная ссылка для сброса пароля")

        self.user = user
        return attrs

    def save(self):
        user = self.user
        user.set_password(self.validated_data['password'])
        user.save()
