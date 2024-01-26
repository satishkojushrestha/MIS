from django.core.exceptions import ValidationError, RequestAborted
from django.utils.translation import gettext_lazy as _

class RegistrationNotImplemented(BaseException):
    """
        Raise if registration model is not implemented on child class
    """
    pass


class ValidationException:
    status_code = 403

    @classmethod
    def raise_validation_error(cls, message):
        raise ValidationError(_(message), cls.status_code)
    
    @classmethod
    def raise_bad_request_error(cls, message, status_code=None):
        raise RequestAborted(_(message), status_code or cls.status_code)