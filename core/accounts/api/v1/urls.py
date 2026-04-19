from django.urls import include, path
from . import views

app_name = 'api-v1'

urlpatterns = [
    # Registration
    path('registration/', views.RegistrationApiView.as_view(), name="registration")
    # Change Password
    # Reset password
    # Login Token
    # Login JWT
    # 
]