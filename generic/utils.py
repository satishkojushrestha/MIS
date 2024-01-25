from abc import abstractmethod
from .exceptions import RegistrationNotImplemented
import re

class Register:

    @staticmethod
    def registration_form(*args, **kwargs):
        raise RegistrationNotImplemented
    
    @staticmethod
    def validate_unique_users(self): ...


class Authentication:
    ...


def number_validator(phone):
    re_pattern = re.compile('^9(04|84|86|85|80|81|82|70|72|74|75|76|88|61|62)[0-9]{7}$')
    re_match = re.match(re_pattern, phone)
    return re_match

def validate_year(year):
    re_pattern1 = re.compile('^19[0-9]{2}$')
    re_pattern2 = re.compile('^20[0-2]{1}[0-3]{1}$')
    