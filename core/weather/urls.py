from django.urls import include, path

app_name = "weather"

urlpatterns = [
    path("api/v1/", include("weather.api.v1.urls")),
    path("api/v2/", include("weather.api.v2.urls")),
]
