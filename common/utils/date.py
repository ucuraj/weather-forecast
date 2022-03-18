from datetime import datetime

from django.utils import timezone


def get_date():
    return timezone.now().date()


def format_date_string(date: str, f_input="%Y-%m-%dT%H:%M:%SZ", f_output="%d/%m/%Y %H:%M"):
    """Recibe una fecha(str) y su formato.
    Devuelve un string en formato DD-MM-AAAA hh:mm."""

    return datetime.strptime(date, f_input).strftime(f_output)


def string_to_date(date: str, f_input="%Y-%m-%dT%H:%M:%S"):
    """Recibe un string y un formato.
    Devuelve una fecha en formato DD-MM-AAAA hh:mm."""

    return datetime.strptime(date, f_input)


def date_to_string(date: datetime, f_output="%Y-%m-%dT%H:%M:%S"):
    """Recibe una fecha(datetime) y un formato de salida.
    Devuelve un string en formato YYYY-MM-AAAAThh:mm:ss."""
    return date.strftime(f_output)


def timestamp_to_date(value):
    if value and isinstance(value, datetime) is False:
        return datetime.fromtimestamp(float(value))
    return None