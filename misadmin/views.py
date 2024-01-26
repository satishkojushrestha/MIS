from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from generic.views import GenericListView
from django.shortcuts import render, redirect
from generic.utils import Register
from .forms import RegistrationForm

class DashboardView(GenericListView):

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
            cleaned_data = registration_form.cleaned_data
            if not self.validate_unique_users(cleaned_data):
                return render(request, 'registration.html',
                      self.format_resp(
                          registration_form=self.registration_form(),
                          message="User Already Registered."
                      ))

        return render(request, 'registration.html', 
                      self.format_resp(
                          registration_form=registration_form                        
                      ))