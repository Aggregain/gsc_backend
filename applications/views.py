from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView

from applications.serializers import ApplicationCreateSerializer, ApplicationListSerializer
from .constants import StatusChoices
from .models import Application

User = get_user_model()


class BaseApplicationMixin(GenericAPIView):
    queryset = Application.objects.prefetch_related('attachments', ).select_related(
        'owner', 'assignee', 'program', 'program__education_place', 'program__education_place__city',
        'program__education_place__city__country').all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        if self.request.user.is_staff:
            return self.queryset.filter(assignee=self.request.user)
        return self.queryset.filter(owner=self.request.user)


class ApplicationRetrieveUpdateDestroyAPIView(BaseApplicationMixin, RetrieveDestroyAPIView):
    ...


class ApplicationListCreateAPIView(BaseApplicationMixin, ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicationListSerializer
        return ApplicationCreateSerializer

    def perform_create(self, serializer):
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            raise APIException('Superuser account not found.')
        serializer.save(owner=self.request.user, status=StatusChoices.draft, assignee=superuser)
