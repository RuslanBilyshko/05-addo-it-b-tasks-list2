from datetime import datetime
from helpers import is_date_past, is_time_past, is_date_now
from wtforms import validators
from models import BaseModel


class DataRequired(validators.DataRequired):
    pass


class Length(validators.Length):
    pass


class Regexp(validators.Regexp):
    pass


class EqualTo(validators.EqualTo):
    pass


class ValidationError(validators.ValidationError):
    pass


class Unique(object):
    """ validator that checks field uniqueness """

    def __init__(self, model: BaseModel, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.filter(getattr(self.model, self.field) == field.data).first()
        if check is not None:
            raise ValidationError(self.message)


class DatePast(object):
    """ validator that checks after Date"""

    def __init__(self, message=None):
        if not message:
            message = u'Date can not be in the past'
        self.message = message

    def __call__(self, form, field):
        check = is_date_past(field.data)
        if check:
            raise ValidationError(self.message)


class TimePast(object):
    """ validator that checks after Time"""

    def __init__(self, date_field_name="date", message=None):
        self.date_field_name = date_field_name
        if not message:
            message = u'Time can not be in the past'
        self.message = message

    def __call__(self, form, field):
        check_date_now = is_date_now(form[self.date_field_name].data)
        check = is_time_past(field.data)
        if check and check_date_now:
            raise ValidationError(self.message)
