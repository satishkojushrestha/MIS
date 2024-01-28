from abc import abstractmethod
from .exceptions import RegistrationNotImplemented
import re
from misadmin.models import User
from django.db import connection
import hashlib
import random
from datetime import datetime
from .connections import DatabaseConnection

class Encrypt:
    
    def create_hash(self, data):
        __algo = hashlib.sha256()
        __algo.update(data.encode())
        return __algo.hexdigest()

    def check_hash(self, data, db_data):
        hash = self.create_hash(data)
        return hash == db_data 
    
    
def generate_username(f_name, l_name):
    n1 = random.randint(1,100)
    n2 = random.randint(100,1000)
    date_time = str(datetime.today())
    return f"{f_name}-{n1}-{l_name}-{date_time}-{n2}"


class Register(Encrypt):
    error_messages = {}
    cleaned_data = {}

    @staticmethod
    def registration_form(*args, **kwargs):
        raise RegistrationNotImplemented
    
    def append_error(self, **kwargs):
        _ = [self.error_messages.update({f'{key}': f'{value}'}) for key, value in kwargs.items()]
        return 
    
    def validate_unique_users(self):
        self.error_messages = {}
        valid_email = True
        valid_phone = True
        email, phone = self.cleaned_data.get('email'), self.cleaned_data.get('phone')
        query = """
                SELECT id FROM misadmin_user
                """
        query_user_email = query + """WHERE email = %s"""
        query_user_phone = query + """WHERE phone = %s"""

        with DatabaseConnection() as db:
            db.execute_query(query_user_email, [email])
            user_e = db.get_id()
            if user_e:
                valid_email = False
                self.append_error(
                    email_error="User with the same email is already registered."
                    )
                
            db.execute_query(query_user_phone, [phone])
            user_p = db.get_id()
            if user_p:
                valid_phone = False
                self.append_error(
                    phone_error="User with the same number is already registered."
                    )            
        return valid_email and valid_phone
    
    def register_user(self):
        if not self.cleaned_data:
            self.append_error(
                error="There has been some error please re-register"
            )
            return
        password = self.create_hash(self.cleaned_data.pop('password'))
        f_name = self.cleaned_data['first_name']
        l_name = self.cleaned_data['last_name']
        username = generate_username(f_name, l_name)
        current_date = datetime.now()
        params = [
            f_name, l_name,  self.cleaned_data['email'], 
            password,  self.cleaned_data['phone'], self.cleaned_data['dob'], 
            self.cleaned_data['gender'],  self.cleaned_data['address'], "true",
            "true", username, "false", "true", current_date, current_date, current_date
        ]
        # performing create operation
        with connection.cursor() as db:
            db.execute(
                """
                    INSERT INTO misadmin_user(first_name, last_name, email, password, phone, dob, gender, address, is_admin, is_superuser, username, is_staff, is_active, date_joined, created_at, updated_at)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                params
                )
            connection.commit()
        return True

class Authentication(Encrypt):
    error_message = ""
    cleaned_data = {}
    user = ""

    @staticmethod
    def login_form(*args, **kwargs):
        raise NotImplementedError
    
    def validate_request(self):
        self.error_message = ""
        if not self.cleaned_data:
            self.error_message = "There has been some error. Please try again later."
            return False
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_query = "SELECT * FROM misadmin_user where email=%s OR phone=%s"
        with DatabaseConnection() as db:
            db.execute_query(user_query, [username, username])
            user = db.filter_query()[0]
            self.user = User(**user)
            if not user:
                self.error_message = "Username or password is incorrect."
                return False
            db_password = user.get('password')
            if not self.check_hash(password, db_password):
                self.error_message = "Invalid Credentials."
                return False
        return True


def number_validator(phone):
    re_pattern = re.compile('^9(04|84|86|85|80|81|82|70|72|74|75|76|88|61|62)[0-9]{7}$')
    re_match = re.match(re_pattern, phone)
    return re_match

# def year_validator(year):
#     re_pattern1 = re.compile('^19[0-9]{2}$')
#     re_pattern2 = re.compile('^20[0-2]{1}[0-3]{1}$')
    