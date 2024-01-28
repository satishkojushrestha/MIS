from django.urls import path
from .views import DashboardView, RegistrationView, LoginView, UsersView, AlbumsView, logout_user
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('mis-admin/', login_required(DashboardView.as_view(), login_url="login"), name='dashboard'),
    path('mis-admin/register', RegistrationView.as_view(), name='register'),
    path('mis-admin/login', LoginView.as_view(), name='login'),
    path('mis-admin/users', login_required(UsersView.as_view(), login_url="login"), name='users'),
    path('mis-admin/albums', login_required(AlbumsView.as_view(), login_url="login"), name='albums'),
    path('mis-admin/logout', logout_user, name='logout'),

]