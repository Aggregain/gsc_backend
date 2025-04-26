from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, GenericAPIView

from accounts.permissions import IsOwnerOrAdminPermission
from .models import WishlistItem
from .serializers import WishlistItemSerializer, WishlistItemCreateSerializer


class QuerySetMixin(GenericAPIView):
    def get_queryset(self):
        return (WishlistItem.objects.select_related('account',
                                                    'program',
                                                    'program__education_place',
                                                    'program__education_place__city',
                                                    'program__education_place__city__country',

                                                    ).prefetch_related('program__academic_requirements',
                                                                       'program__education_place__expenses',
                                                                       'program__education_place__deadlines')
                .filter(account=self.request.user))



class WishListView(QuerySetMixin, ListAPIView):
    serializer_class = WishlistItemSerializer


class WishAddView(QuerySetMixin, CreateAPIView):
    serializer_class = WishlistItemCreateSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(account=self.request.user)
        except IntegrityError as e:
            raise ValidationError({"detail": "Database integrity error.", "error": str(e)})

class WishDeleteView(QuerySetMixin, DestroyAPIView):
    permission_classes = [IsOwnerOrAdminPermission, ]
