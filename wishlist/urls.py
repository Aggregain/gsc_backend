from django.urls import path
from . import views
app_name = 'wishlist'

urlpatterns = [
    path('items/', views.WishListView.as_view(), name='items'),
    path('add/', views.WishAddView.as_view(), name='add'),
    path('delete/<int:pk>', views.WishDeleteView.as_view(), name='delete'),
]