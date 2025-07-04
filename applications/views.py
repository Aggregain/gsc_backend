from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from applications.serializers import ApplicationCreateSerializer, ApplicationListSerializer, ApplicationRetrieveUpdateSerializer
from .constants import StatusChoices
from .filters import ApplicationFilter
from .models import Application
from .permissions import ApplicationEditPermission

User = get_user_model()


class BaseApplicationMixin(GenericAPIView):
    queryset = Application.objects.prefetch_related('attachments',).select_related(
        'owner', 'assignee', 'program', 'program__education_place', 'program__education_place__city',
        'program__education_place__city__country').all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        if self.request.user.is_staff:
            return self.queryset.filter(assignee=self.request.user)
        return self.queryset.filter(owner=self.request.user)


class ApplicationRetrieveUpdateDestroyAPIView(BaseApplicationMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated, ApplicationEditPermission,]





class ApplicationListCreateAPIView(BaseApplicationMixin, ListCreateAPIView):

    filterset_class = ApplicationFilter
    ordering_fields = '__all__'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicationListSerializer
        return ApplicationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            raise NotAcceptable('Аккаунт суперпользователя не найден')
        application = serializer.save(owner=self.request.user,
                                      status=StatusChoices.DRAFT,
                                      assignee=superuser)
        return Response(ApplicationListSerializer(application).data, status=201)


    def get_serializer_context(self):
        ctxt = super().get_serializer_context()
        ctxt['request'] = self.request
        return ctxt


