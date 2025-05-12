from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from notifications.models import Notification
from notifications.serializers import NotificationSerializer, NotificationListSerializer


class NotificationAPIView(APIView):
    serializer_class = NotificationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)

class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.select_related('application', 'receiver', )