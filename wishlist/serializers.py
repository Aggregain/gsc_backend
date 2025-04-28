

from rest_framework.serializers import ModelSerializer

from common.serializers import EducationPlaceSerializer
from .models import WishlistItem


class WishlistItemSerializer(ModelSerializer):
    education_place = EducationPlaceSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        exclude = ['account', ]

class WishlistItemCreateSerializer(ModelSerializer):

    class Meta:
        model = WishlistItem
        fields = '__all__'
        read_only_fields = ['account', ]

