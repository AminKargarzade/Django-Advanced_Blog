import requests
from django.core.cache import cache
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

WEATHER_CACHE_TIMEOUT = 20 * 60  # 20 دقیقه به ثانیه


weather_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "city": openapi.Schema(type=openapi.TYPE_STRING, description="نام شهر"),
        "country": openapi.Schema(
            type=openapi.TYPE_STRING, description="کد کشور (مثلاً IR)"
        ),
        "temperature": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="دما به سانتیگراد"
        ),
        "feels_like": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="دمای احساسی"
        ),
        "humidity": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="رطوبت (درصد)"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="توضیح وضعیت هوا"
        ),
        "wind_speed": openapi.Schema(
            type=openapi.TYPE_NUMBER, description="سرعت باد (متر/ثانیه)"
        ),
        "cached": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="آیا از cache برگشته؟"
        ),
    },
)


class WeatherAPIView(APIView):

    @swagger_auto_schema(
        operation_description=(
            "با دادن نام هر شهری در جهان， "
            "وضعیت فعلی آب‌وهوا رو برمی‌گردونه. "
            "داده‌ها **۲۰ دقیقه** در Redis کش می‌شن."
        ),
        manual_parameters=[
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,
                description="نام شهر به انگلیسی — مثال: Tehran، London، Tokyo",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="داده آب‌وهوا با موفقیت برگشت",
                schema=weather_response_schema,
            ),
            400: openapi.Response(description="پارامتر city ارسال نشده"),
            404: openapi.Response(description="شهر پیدا نشد"),
            503: openapi.Response(description="خطا در اتصال به OpenWeather"),
            504: openapi.Response(description="Timeout اتصال"),
        },
        tags=["🌤 Weather"],
    )
    def get(self, request):
        city = request.query_params.get("city", "").strip()

        if not city:
            return Response(
                {"error": "پارامتر city الزامی است"}, status=status.HTTP_400_BAD_REQUEST
            )

        # ساخت کلید یکتا برای cache
        cache_key = f"weather::{city.lower().replace(' ', '_')}"

        # بررسی cache
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data["cached"] = True
            return Response(cached_data, status=status.HTTP_200_OK)

        # درخواست به OpenWeather
        try:
            response = requests.get(
                url="https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city,
                    "appid": settings.OPENWEATHERMAP_API_KEY,
                    "units": "metric",  # دمای سانتیگراد
                    "lang": "en",
                },
                timeout=10,
            )

            if response.status_code == 404:
                return Response(
                    {"error": f'شهر "{city}" در OpenWeather پیدا نشد'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response.raise_for_status()
            data = response.json()

            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "wind_speed": data["wind"]["speed"],
                "cached": False,
            }

            # ذخیره در cache برای ۲۰ دقیقه
            cache.set(cache_key, weather_data, WEATHER_CACHE_TIMEOUT)

            return Response(weather_data, status=status.HTTP_200_OK)

        except requests.exceptions.Timeout:
            return Response(
                {"error": "Timeout — OpenWeather جواب نداد"},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except requests.exceptions.ConnectionError:
            return Response(
                {"error": "خطا در اتصال به OpenWeather"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
