from abc import abstractmethod
from .exceptions import RegistrationNotImplemented
import re
from misadmin.models import User
from django.db import connection
import hashlib

class Encrypt:
    
    algo = hashlib.sha256()

    def create_hash(self, data):
        self.algo.update(data.encode())
        return self.algo.hexdigest()

    def check_hash(self, data, db_data):
        hash = self.create_hash(data)
        return hash == db_data 
    

class Register(Encrypt):
    error_messages = {}
    cleaned_data = {}

    @staticmethod
    def registration_form(*args, **kwargs):
        raise RegistrationNotImplemented
    
    def append_error(self, **kwargs):
        _ = [self.error_messages.update(f'{key}: {value}') for key, value in kwargs.items()]
        return 
    
    def validate_unique_users(self):
        email, phone = self.cleaned_data.get('email'), self.cleaned_data.get('phone')
        query = """
                SELECT id FROM misadmin_user
                """
        query_user_email = query + """WHERE email = %s"""
        user_e = User.objects.raw(
            query_user_email, [email]
        )
        if len(user_e) > 0:
            self.append_error(
                email_error="User with the same email is already registered."
                )
        query_user_phone = query + """WHERE phone = %s"""
        user_p = User.objects.raw(
            query_user_phone, [phone]
        )
        if len(user_p) > 0:
            self.append_error(
                phone_error="User with the same number is already registered."
                )
        return
    
    def register_user(self):
        if not self.cleaned_data:
            self.append_error(
                error="There has been some error please re-register"
            )
            return
        password = self.check_hash(self.cleaned_data.pop('password'))
        # performing create operation
        with connection.cursor() as db:
            db.execute(
                """
                    INSERT INTO misadmin_user(first_name, last_name, email, password, phone, dob, gender, address, is_admin)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%b)
                """,
                [self.cleaned_data['first_name'], self.cleaned_data['last_name'], self.cleaned_data['email'], password, self.cleaned_data['phone'], self.cleaned_data['dob'], self.cleaned_data['gender'], self.cleaned_data['address'], True]
                )
        connection.commit()
        return True

class Authentication:
    ...


def number_validator(phone):
    re_pattern = re.compile('^9(04|84|86|85|80|81|82|70|72|74|75|76|88|61|62)[0-9]{7}$')
    re_match = re.match(re_pattern, phone)
    return re_match

def year_validator(year):
    re_pattern1 = re.compile('^19[0-9]{2}$')
    re_pattern2 = re.compile('^20[0-2]{1}[0-3]{1}$')
    