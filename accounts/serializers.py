from django.db.utils import IntegrityError

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Attachment
from django.db.transaction import atomic

class AttachmentWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    grade = serializers.DecimalField(required=False, max_digits=5, decimal_places=2)
    file = serializers.FileField(required=False, allow_null=True)
    meta = serializers.JSONField(required=False)


class CreateAccountSerializer(serializers.ModelSerializer):
    attachments = serializers.DictField(child=AttachmentWriteSerializer(), required=False)
    class Meta:
        model = get_user_model()

        exclude = ['last_login', 'is_active', 'groups', 'user_permissions']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True,

                'style': {'input_type': 'password'}
            }
        }


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['attachments'] = {
            attachment.name: {
                "id": attachment.id,
                "file": attachment.file.url if attachment.file else None,
                "grade": attachment.grade,
                "meta": attachment.meta,
            }
            for attachment in instance.attachments.all()
        }
        return representation

    def _create_or_update_attachments(self, account, attachments_data):
        for name, data in attachments_data.items():
            attachment_id = data.pop("id", None)
            if attachment_id:
                attachment = Attachment.objects.filter(id=attachment_id,account=account).first()
                if attachment:
                    for attr, value in data.items():
                        setattr(attachment, attr, value)
                    attachment.save()
            else:
                try:
                    Attachment.objects.create(
                        account=account,
                        name=name,
                       **data
                    )
                except IntegrityError:
                    raise serializers.ValidationError(f"Attachment {name} already exists")

    @atomic
    def update(self, instance, validated_data):
        attachments_data = validated_data.pop('attachments', {})
        instance = self.update_user(instance, validated_data)
        self._create_or_update_attachments(instance, attachments_data)
        return instance

    @atomic
    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', {})
        account = get_user_model().objects.create_user(**validated_data)
        self._create_or_update_attachments(account, attachments_data)
        return account


    def update_user(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user



