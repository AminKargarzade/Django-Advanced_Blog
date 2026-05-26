from django.urls import path
from .. import views

# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Registration
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    path("test-email/", views.TestEmailSend.as_view(), name="test-email"),
    # Activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # Resend Activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # Change Password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Reset password
    path(
        "reset-password/",
        views.ResetPasswordApiView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/confirm/<str:uid>/<str:token>",
        views.ResetPasswordConfirmApiView.as_view(),
        name="reset-password-confirm",
    ),
    # Login Token
    # path(
    #     "token/login/",
    #     views.CustomObtainAuthToken.as_view(),
    #     name="token-login",
    # ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # Login JWT
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
