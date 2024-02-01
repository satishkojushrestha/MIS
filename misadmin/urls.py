from django.urls import path
from .views import DashboardView, RegistrationView, LoginView, UsersView, ArtistsView, logout_user, ArtistMusicView, MusicView, index
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('mis-admin/', login_required(DashboardView.as_view(), login_url="login"), name='dashboard'),
    path('mis-admin/register', RegistrationView.as_view(), name='register'),
    path('mis-admin/login', LoginView.as_view(), name='login'),
    path('mis-admin/users', login_required(UsersView.as_view(), login_url="login"), name='users'),
    path('mis-admin/users/<str:identifier>', login_required(UsersView.as_view(), login_url="login"), name='user_actions'),
    path('mis-admin/users/delete/<str:id>', login_required(UsersView.as_view(), login_url="login"), name='delete_user'),
    path('mis-admin/artists', login_required(ArtistsView.as_view(), login_url="login"), name='artists'),
    path('mis-admin/artists/<str:identifier>', login_required(ArtistsView.as_view(), login_url="login"), name='artist_actions'),
    path('mis-admin/artists/delete/<str:id>', login_required(ArtistsView.as_view(), login_url="login"), name='delete_artist'),
    path('mis-admin/music/<int:id>', login_required(ArtistMusicView.as_view(), login_url="login"), name='music'),
    path('mis-admin/music/<str:identifier>/<int:artist_id>', login_required(MusicView.as_view(), login_url="login"), name='music_actions'),
    path('mis-admin/deletemusic/delete/<str:id>', login_required(MusicView.as_view(), login_url="login"), name='delete_music'),
    path('mis-admin/logout', logout_user, name='logout'),
    path('', index, name='index')
]