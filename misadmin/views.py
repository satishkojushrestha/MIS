from generic.views import GenericListView, GenericView
from django.shortcuts import render, redirect
from generic.utils import Register
from .forms import RegistrationForm

class DashboardView(GenericView):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')
    

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
                request.session['registration_message'] = {"header": "Success Message", "message": "You have registered successfully."}
                return redirect("login")

        return render(request, 'registration.html', 
                      self.format_resp(
                          registration_form=registration_form,
                          error_messages=self.error_messages
                      ))
    

class LoginView(GenericListView):
    
    def get(self, request, *args, **kwargs):
        registration_message = request.session.pop('registration_message', None)
        return render(request, 'login.html',
                      self.format_resp(
                          registration_message=registration_message
                      ))