import requests
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from apps.oraculum.models import FORECAST_CHOICES, FORECAST_CHOICES_REVERSE
from common.utils.requests import format_query_params

from django.template.defaulttags import register


@register.filter
def get_forecast_type(key):
    return FORECAST_CHOICES_REVERSE.get(key)


def make_request(request, params):
    api_url = request.build_absolute_uri(reverse("weather-forecast-api-v1-get-forecast"))
    try:
        data = requests.get(f'{api_url}?{params}').json()

        return data
    except requests.HTTPError:
        return {"data": "Error fetching data. Try again"}


def forecast_weather_view(request):
    context = {
        "forecast_types": FORECAST_CHOICES,
        "maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "forecast_type": request.GET.get("forecast_type")
    }
    if request.GET.get("do_request") == "true":
        valid_qp = ["lat", "lon", "forecast_type"]
        context["forecast_data"] = make_request(request, format_query_params(request.GET, valid_qp))

    return render(request, "oraculum/home.html", context)
