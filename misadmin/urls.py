from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('mis-admin/', DashboardView.as_view(), name='dashboard'),
]