from django.urls import path
from . import views
app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListAPIView.as_view(), name='list'),
    path('read/', views.NotificationAPIView.as_view(), name='read'),
]