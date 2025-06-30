from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, GenericAPIView

from accounts.permissions import IsOwnerOrAdminPermission
from .models import WishlistItem
from .serializers import WishlistItemSerializer, WishlistItemCreateSerializer


class QuerySetMixin(GenericAPIView):
    def get_queryset(self):
        return (WishlistItem.objects.select_related('account',
                                                    'education_place',
                                                    'education_place__city',
                                                    'education_place__city__country',

                                                    ).prefetch_related('education_place__degrees',
                                                                       'education_place__degrees__academic_requirements',
                                                                       'education_place__degrees__deadlines',
                                                                       'education_place__degrees__expenses',
                                                                       )
                .filter(account=self.request.user))


class WishlistCreateListView(QuerySetMixin, ListAPIView, CreateAPIView):
    serializer_class = WishlistItemCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WishlistItemSerializer
        return WishlistItemCreateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(account=self.request.user)
        except IntegrityError as e:
            raise ValidationError({"detail": "Database integrity error.", "error": str(e)})


class WishDeleteView(QuerySetMixin, DestroyAPIView):
    permission_classes = [IsOwnerOrAdminPermission, ]
