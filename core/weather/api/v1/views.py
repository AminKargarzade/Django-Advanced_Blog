import logging

import requests
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import WeatherSerializer
from weather.services import WeatherService

logger = logging.getLogger(__name__)


class WeatherAPIView(APIView):

    city_param = openapi.Parameter(
        "city",
        openapi.IN_QUERY,
        description="Enter city name",
        type=openapi.TYPE_STRING,
        required=True,
    )

    @swagger_auto_schema(
        manual_parameters=[city_param],
        tags=["🌤 Weather"],
    )
    def get(self, request):

        serializer = WeatherSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data["city"]

        cache_key = f"weather_{city.lower()}"

        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Weather data for '{city}' loaded from cache")
            return Response(cached_data)

        try:
            logger.info(f"Fetching weather data for '{city}' from OpenWeather")

            data = WeatherService.get_weather(city)

            cache.set(
                cache_key,
                data,
                timeout=1200,
            )

            logger.info(f"Weather data for '{city}' cached successfully")

            return Response(data)

        except requests.HTTPError:
            logger.warning(f"City '{city}' not found")

            return Response(
                {"detail": "City not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except requests.RequestException:
            logger.error(
                f"OpenWeather service unavailable for city '{city}'",
                exc_info=True,
            )

            return Response(
                {"detail": "Weather service unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except Exception:
            logger.exception("Unexpected error occurred")

            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
