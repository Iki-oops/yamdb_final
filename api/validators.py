import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def my_year_validator(value):
    if value > dt.datetime.now().year:
        raise ValidationError(_('%(value)s is not a correct year!'),
                              params={'value': value},)
