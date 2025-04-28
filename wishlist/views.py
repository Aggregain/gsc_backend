from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from accounts.permissions import IsOwnerOrAdminPermission
from .models import WishlistItem
from .serializers import WishlistItemSerializer, WishlistItemCreateSerializer


class WishListView(ListAPIView):
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        return (WishlistItem.objects.select_related('account',
                                                    'education_place',
                                                    'education_place__city',
                                                    'education_place__city__country',


                                                    ).prefetch_related('education_place__deadlines',
                                                                       'education_place__degrees',
                                                                       'education_place__expenses')
                .filter(account=self.request.user))


class WishAddView(CreateAPIView):
    serializer_class = WishlistItemCreateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(account=self.request.user)
        except IntegrityError as e:
            raise ValidationError({"detail": "Database integrity error.", "error": str(e)})


class WishDeleteView(DestroyAPIView):
    permission_classes = [IsOwnerOrAdminPermission, ]
