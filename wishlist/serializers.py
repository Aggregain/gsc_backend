

from rest_framework.serializers import ModelSerializer
from .models import WishlistItem
from common.serializers import ProgramSerializer

class WishlistItemSerializer(ModelSerializer):
    program = ProgramSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        exclude = ['account', ]

class WishlistItemCreateSerializer(ModelSerializer):

    class Meta:
        model = WishlistItem
        fields = '__all__'
        read_only_fields = ['account', ]

