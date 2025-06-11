from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Attachment, Account
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
    phone_number = serializers.CharField(max_length=19, validators=[validate_phone_number])
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
        adjusted_number = adjust_phone_number(validated_data['phone_number'])
        validated_data['phone_number'] = adjusted_number
        return get_user_model().objects.create_user(**validated_data)

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
