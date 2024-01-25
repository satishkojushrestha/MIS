from django.urls import path
from .views import DashboardView, RegistrationView

urlpatterns = [
    path('mis-admin/', DashboardView.as_view(), name='dashboard'),
    path('mis-admin/register', RegistrationView.as_view(), name='register'),
]