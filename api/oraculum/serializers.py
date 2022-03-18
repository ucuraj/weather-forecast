from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers

from api.oraculum.models import WeatherForecast


class OraculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = (
            'time_zone',
            'time_zone_offseet',
            'lat',
            'lon',
            'dt',
            'raw_data',
        )


class OraculumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = (
            'lat',
            'lon',
            'forecast_type'
        )
