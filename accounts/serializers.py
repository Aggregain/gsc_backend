from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = ['account', ]
        read_only_fields = ['id', ]


class AccountSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    class Meta:
        model = get_user_model()

        fields = ['first_name', 'second_name', 'last_name', 'email', 'avatar',
                  'degree', 'gre_grade', 'gmat_grade', 'duolingo_grade', 'sat_grade',
                  'toefl_grade', 'toefl_grade', 'ielts_grade', 'education_place',
                  'country', 'city', 'birth_date', 'phone_number']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True,

                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user




class AvatarEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar', ]


class GoogleTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
