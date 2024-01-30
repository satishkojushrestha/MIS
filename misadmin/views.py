from generic.views import GenericListView, GenericView
from django.shortcuts import render, redirect
from generic.utils import Register, Authentication
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout
from generic.connections import DatabaseConnection

class DashboardView(GenericView):

    def get(self, request, *args, **kwargs):

        return render(request, 'dashboard.html')
    

class RegistrationView(GenericListView, Register):

    @staticmethod
    def registration_form(*args, **kwargs):
        return RegistrationForm(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'registration.html',
                      self.format_resp(
                          registration_form=self.registration_form()
                      ))
    
    def post(self, request, *args, **kwargs):
        registration_form = self.registration_form(request.POST)
        if registration_form.is_valid():
            self.cleaned_data = registration_form.cleaned_data
            if not self.validate_unique_users():
                return render(request, 'registration.html',
                      self.format_resp(
                          registration_form=registration_form,
                          error_messages=self.error_messages
                      ))
            if self.register_user():
                request.session['registration_message'] = {"header": "Registration Completed", "message": "You have registered successfully."}
                return redirect("login")

        return render(request, 'registration.html', 
                      self.format_resp(
                          registration_form=registration_form,
                          error_messages=self.error_messages
                      ))
    

class LoginView(GenericListView, Authentication):

    @staticmethod
    def login_form(*args, **kwargs):
        return LoginForm(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        registration_message = request.session.pop('registration_message', None)
        return render(request, 'login.html',
                      self.format_resp(
                          registration_message=registration_message,
                          login_form = self.login_form()
                      ))
    
    def post(self, request, *args, **kwargs):
        login_form = self.login_form(request.POST)
        if login_form.is_valid():
            self.cleaned_data = login_form.cleaned_data
            valid = self.validate_request()
            if valid:
                try:
                    login(request, self.user)
                    return redirect('dashboard')
                except:
                    self.error_message = "There has been some error. Please relogin"
                
        return render(request, 'login.html', 
                              self.format_resp(
                                error_message = self.error_message,
                                login_form = login_form
                              )) 
    

class UsersView(GenericListView):  

    @staticmethod
    def generate_pagination_list(current_page, total_pages, max_pages_display=5):
        if total_pages <= max_pages_display:
            return list(range(1, total_pages + 1))

        half_max = max_pages_display // 2

        if current_page - half_max <= 0:
            return list(range(1, max_pages_display + 1))

        if current_page + half_max > total_pages:
            return list(range(total_pages - max_pages_display + 1, total_pages + 1))

        return list(range(current_page - half_max, current_page + half_max + 1))


    def get(self, request, *args, **kwargs):
        if kwargs:
            identifier = kwargs['identifier']
            if not isinstance(identifier, str):
                try:
                    identifier = int(identifier)
                except:
                    #render 404 page
                    ...
            if identifier == 'add':
                return render(request, 'user_dynamic_form.html', {
                    'form': RegistrationForm(),
                    'current_page': 'Add User',
                    'form_title': 'Create User',
                })
            else:
              #render 404 page
                ...  
        selected_page = request.GET.get('page')
        try:
            selected_page = int(selected_page)
        except:
            selected_page = None
        context = {}
        with DatabaseConnection() as db:
            # db.execute_query(user_query)
            # users = db.filter_query()
            data = db.execute_paginate_query("misadmin_user", per_page=3, page=selected_page)
            context['users'] = data['datas']
            context['per_page'] = data['per_page']
            context['page'] = data['page']
            context['total_pages'] = data['total_pages']
        pagination_list = self.generate_pagination_list(context['page'], context['total_pages'])
        context['pagination_list'] = pagination_list
        return render(request, 'users.html', context)
    

class ArtistsView(GenericListView):

    def get(self, request, *args, **kwargs):
        return render(request, 'artists.html')
    

def logout_user(request):
    logout(request)
    return redirect('login')
