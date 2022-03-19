from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers

from apps.oraculum.models import WeatherForecast, FORECAST_CHOICES


class WeatherForecastSerializer(serializers.Serializer):
    lat = serializers.DecimalField(decimal_places=4, max_digits=16, required=True)
    lon = serializers.DecimalField(decimal_places=4, max_digits=16, required=True)
    forecast_type = serializers.ChoiceField(choices=FORECAST_CHOICES, required=True)

    class Meta:
        fields = (
            'lat',
            'lon',
            'forecast_type'
        )


class WeatherForecastDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = (
            'time_zone',
            'time_zone_offset',
            'lat',
            'lon',
            'dt',
            'raw_data',
        )
