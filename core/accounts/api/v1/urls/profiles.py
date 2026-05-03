from django.urls import path
from .. import views

urlpatterns = [
    # Profile
    path("", views.ProfileApiView.as_view(), name="profile"),
]
