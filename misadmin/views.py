from generic.views import GenericListView, GenericView
from django.shortcuts import render, redirect
from generic.utils import Register, Authentication
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout

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

    def get(self, request, *args, **kwargs):
        return render(request, 'users.html')
    

class AlbumsView(GenericListView):

    def get(self, request, *args, **kwargs):
        return render(request, 'albums.html')
    

def logout_user(request):
    logout(request)
    return redirect('login')
