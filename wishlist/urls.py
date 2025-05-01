from django.urls import path
from . import views
app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistCreateListView.as_view(), name='wishlist-create-list'),

    path('<int:pk>', views.WishDeleteView.as_view(), name='wishlist-delete'),
]