from rest_framework import serializers
from django.shortcuts import get_object_or_404

from applications.models import Application
from notifications.models import Notification


class NotificationSerializer(serializers.Serializer):
    application_id = serializers.IntegerField(required=True)

    def save(self, **kwargs):
        application_id = self.validated_data['application_id']
        application = get_object_or_404(Application, pk=application_id)
        application.notifications.all().update(is_seen=True)


class NotificationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'