from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = ['account', ]
        read_only_fields = ['id', ]


class AccountReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        exclude = ['last_login', 'is_active', 'groups', 'user_permissions', ]
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


class AccountEditSerializer(AccountReadSerializer):
    class Meta(AccountReadSerializer.Meta):
        exclude = AccountReadSerializer.Meta.exclude + ['avatar', ]


class AvatarEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar', ]


class GoogleTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
