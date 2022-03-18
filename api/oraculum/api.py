from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.oraculum.models import WeatherForecast
from api.oraculum.serializers import OraculumSerializer, OraculumCreateSerializer
from common.utils.views import GenericOptionalPageViewSet


class OraculumViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericOptionalPageViewSet):
    queryset = WeatherForecast.objects.all()
    serializer_class = OraculumSerializer
    permission_classes = [AllowAny]

    filter_fields = ('lat', 'lon', 'dt', 'forecast_type')
    search_fields = ('lat',)
    ordering_fields = ('forecast_type', 'lat', 'logintude')
    ordering = 'dt'

    serializers = {
        'default': OraculumSerializer,
        'create': OraculumCreateSerializer,

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

        return super(OraculumViewSet, self).list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.query_params.get('no_page'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return super(OraculumViewSet, self).list(self, request, *args, **kwargs)
