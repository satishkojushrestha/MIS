from django.urls import path
from .views import DashboardView, RegistrationView, LoginView

urlpatterns = [
    path('mis-admin/', DashboardView.as_view(), name='dashboard'),
    path('mis-admin/register', RegistrationView.as_view(), name='register'),
    path('mis-admin/login', LoginView.as_view(), name='login'),
]