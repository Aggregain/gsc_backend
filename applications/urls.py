from django.urls import path
from . import views
app_name = 'applications'

urlpatterns = [
    path('', views.ApplicationListCreateAPIView.as_view(), name='application-create-list'),
    path('<int:pk>/', views.ApplicationRetrieveUpdateDestroyAPIView.as_view(), name='application-edit'),
    path('comments/', views.CommentCreateView.as_view(), name='comment-create'),

]