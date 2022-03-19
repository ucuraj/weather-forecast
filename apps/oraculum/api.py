from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.oraculum.models import WeatherForecast, FORECAST_CHOICES_REVERSE
from apps.oraculum.serializers import WeatherForecastSerializer, WeatherForecastDetailSerializer
from apps.oraculum.services import WeatherForecastService
from common.utils.views import GenericOptionalPageViewSet


class WeatherForecastViewSet(mixins.ListModelMixin, GenericOptionalPageViewSet):
    queryset = WeatherForecast.objects.all()
    permission_classes = [AllowAny]

    filter_fields = ('lat', 'lon', 'dt', 'forecast_type')
    search_fields = ('lat',)
    ordering_fields = ('forecast_type', 'lat', 'lon')
    ordering = 'dt'

    serializers = {
        'default': WeatherForecastDetailSerializer,
        'get_forecast': WeatherForecastSerializer,
    }

    def get_serializer_class(self):
        """
        Returns a serializer based on the HTTP verb.
        If not defined, return the default serializer.
        """
        return self.serializers.get(
            self.action, self.serializers["default"])

    def list(self, request, *args, **kwargs):
        if request.query_params.get('no_page'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super(WeatherForecastViewSet, self).list(self, request, *args, **kwargs)

    @action(methods=["GET"], detail=False)
    def forecast_type(self, request, *args, **kwargs):
        return Response(data=FORECAST_CHOICES_REVERSE, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_forecast(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        service = WeatherForecastService()
        instance = service.get_weather_forecast(validated_data)
        return Response(data=WeatherForecastDetailSerializer(instance).data, status=status.HTTP_200_OK)
