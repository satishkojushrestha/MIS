from abc import abstractmethod
from .exceptions import RegistrationNotImplemented
import re
from misadmin.models import User

class Register:

    @staticmethod
    def registration_form(*args, **kwargs):
        raise RegistrationNotImplemented
    
    @staticmethod
    def validate_unique_users(cleaned_data):
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        query = """
            SELECT id FROM misadmin_user 
            WHERE email = %s 
            OR phone = %s
        """
        params = [email, phone]
        user = User.objects.raw(
            query, params
        )
        # query_user_e = """
        #     SELECT id FROM misadmin_user 
        #     WHERE email = %s 
        # """

        # query_user_p = """
        #     SELECT id FROM misadmin_user 
        #     WHERE phone = %s
        # """
        # params = [email, phone]
        # user_e = User.objects.raw(
        #     query_user_e, [email]
        # )
        if not len(user) > 0:
            return False
        else:
            return False


class Authentication:
    ...


def number_validator(phone):
    re_pattern = re.compile('^9(04|84|86|85|80|81|82|70|72|74|75|76|88|61|62)[0-9]{7}$')
    re_match = re.match(re_pattern, phone)
    return re_match

def validate_year(year):
    re_pattern1 = re.compile('^19[0-9]{2}$')
    re_pattern2 = re.compile('^20[0-2]{1}[0-3]{1}$')
    