from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationListSerializer


class NotificationAPIView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationListSerializer
    def get_queryset(self):
        return (Notification.objects.select_related('application', 'receiver', ).
                filter(receiver=self.request.user, is_seen=False).order_by('-created_at'))
