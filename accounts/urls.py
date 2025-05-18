# from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.urls.conf import re_path

from . import views
from .views import  GoogleView

router = DefaultRouter()
router.register(basename='attachments', prefix='attachments', viewset=views.AttachmentViewSet)

urlpatterns = [
    path('register/', views.CreateAccountView.as_view(), name='register'),
    path('profile/', views.ManageAccountView.as_view(), name='profile'),
    path('token/', views.TokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.RefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleView.as_view(), name="google_login"),
    path('avatar/', views.AvatarEditView.as_view(), name="avatar"),
    path('<int:pk>/', views.AccountDetailView.as_view(), name="account-detail"),
    # re_path(r'password/reset/?$', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
] + router.urls
