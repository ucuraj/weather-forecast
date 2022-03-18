from rest_framework import serializers


class UnixEpochDateField(serializers.DateTimeField):
    """Convierte valor recibido en epoch a datetime YYYY-MM-DDThh:mm """

    def to_internal_value(self, value):
        from common.utils.date import string_to_date, timestamp_to_date, date_to_string

        try:
            dt = timestamp_to_date(value)
            date_string = date_to_string(dt)
            return super(UnixEpochDateField, self).to_internal_value(value=date_string)
        except (AttributeError, TypeError, ValueError):
            pass
        self.fail('invalid', format='UnixEpoch')
