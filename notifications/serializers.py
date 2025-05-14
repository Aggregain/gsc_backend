from rest_framework import serializers
from django.shortcuts import get_object_or_404

from applications.models import Application
from applications.serializers import ApplicationRetrieveUpdateSerializer
from notifications.models import Notification


class NotificationSerializer(serializers.Serializer):
    application_id = serializers.IntegerField(required=False)

    def save(self, **kwargs):
        application_id = self.validated_data.get('application_id')
        if application_id:
            application = get_object_or_404(Application, pk=application_id)
            application.notifications.all().update(is_seen=True)
        else:
            user = self.context['request'].user
            user.notifications.all().update(is_seen=True)


class NotificationListSerializer(serializers.ModelSerializer):
    application = ApplicationRetrieveUpdateSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'