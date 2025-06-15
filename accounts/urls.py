from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import GoogleView

router = DefaultRouter()
router.register(basename='attachments', prefix='attachments', viewset=views.AttachmentViewSet)

urlpatterns = [
                  path('register/', views.CreateAccountView.as_view(), name='register'),
                  path('profile/', views.ManageAccountView.as_view(), name='profile'),
                  path('token/', views.TokenView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('google/', GoogleView.as_view(), name="google_login"),
                  path('avatar/', views.AvatarEditView.as_view(), name="avatar"),
                  path('<int:pk>/', views.AccountDetailView.as_view(), name="account-detail"),
                  path('email/confirm/send/', views.ConfirmEmailSendView.as_view(), name="email-confirm-send"),
                  path('email/confirm/<str:uidb64>/<str:token>/', views.EmailConfirmView.as_view(),
                       name='email-confirm'),
                  path('password/reset/', views.PasswordResetView.as_view(), name='password-reset'),
                  path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(),
                       name='password-reset-confirm'),

              ] + router.urls
