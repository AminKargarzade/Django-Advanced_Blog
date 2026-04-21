from django.urls import include, path
from . import views
# from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'api-v1'

urlpatterns = [
    # Registration
    path('registration/', views.RegistrationApiView.as_view(), name="registration"),
    path('token/login/', views.CustomObtainAuthToken.as_view(), name="token-login")
    
    # Change Password
    # Reset password
    
    # Login Token
    # Login JWT 
]