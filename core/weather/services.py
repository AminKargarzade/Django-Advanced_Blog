import requests

from django.conf import settings

# class WeatherService:
#     @staticmethod
#     def get_weather(city):
#         api_key = settings.OPENWEATHERMAP_API_KEY
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 "temperature": data["main"]["temp"],
#                 "description": data["weather"][0]["description"],
#                 "icon": data["weather"][0]["icon"],
#             }
#         else:
#             return None


class WeatherService:

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather(cls, city):

        response = requests.get(
            cls.BASE_URL,
            params={
                "q": city,
                "appid": settings.OPENWEATHERMAP_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )

        response.raise_for_status()

        return response.json()
