from rest_framework import serializers


class WeatherResponseSerializer(serializers.Serializer):
    city = serializers.CharField()
    country = serializers.CharField()
    temperature = serializers.FloatField()
    feels_like = serializers.FloatField()
    humidity = serializers.IntegerField()
    description = serializers.CharField()
    wind_speed = serializers.FloatField()
    cached = serializers.BooleanField(
        help_text="اگه True باشه یعنی داده از cache برگشته"
    )
