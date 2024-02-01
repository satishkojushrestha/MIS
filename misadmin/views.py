from generic.views import GenericListView, GenericView
from django.shortcuts import render, redirect
from generic.utils import Register, Authentication, generate_pagination_list, json_parser
from .forms import RegistrationForm, LoginForm, UserEditForm, ArtistForm, MusicForm
from django.contrib.auth import login, logout
from generic.connections import DatabaseConnection
from django.http import JsonResponse
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect

class DashboardView(GenericView):

    def get(self, request, *args, **kwargs):
        query_user = "SELECT COUNT(id) as count from misadmin_user"
        query_artist = "SELECT COUNT(id) as count from misadmin_artist"
        query_music = "SELECT COUNT(id) as count from misadmin_music"

        with DatabaseConnection() as db:
            db.execute_query(query_user)
            users = db.filter_query()[0]['count']
            db.execute_query(query_artist)
            artists = db.filter_query()[0]['count']
            db.execute_query(query_music)
            musics = db.filter_query()[0]['count']
                
        return render(request, 'dashboard.html',
                      self.format_resp(
                          users=users,
                          artists=artists,
                          musics=musics
                      ))
    

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
                request.session['registration_message'] = {"header": "Registration Completed", 
                                                           "message": "You have registered successfully."}
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
    

class UsersView(GenericListView, Register):  

    def get(self, request, *args, **kwargs):
        if kwargs:
            identifier = kwargs['identifier']            
            try:
                identifier = int(identifier)
                with DatabaseConnection() as db:
                    user = db.get_by_id('misadmin_user', identifier)                    
                registration_form = UserEditForm(user)
                return render(request, 'user_dynamic_form.html', {
                    'form': registration_form,
                    'current_page': 'Edit User',
                    'form_title': 'Update User',
                    'request_method': 'patch',
                    'user_id': identifier
                })

            except:
                ...

            if identifier == 'add':
                return render(request, 'user_dynamic_form.html', {
                    'form': RegistrationForm(),
                    'current_page': 'Add User',
                    'form_title': 'Create User',
                })
        selected_page = request.GET.get('page')
        try:
            selected_page = int(selected_page)
        except:
            selected_page = None
        context = {}
        with DatabaseConnection() as db:
            data = db.execute_paginate_query("misadmin_user", per_page=3, page=selected_page)
            context['users'] = data['datas']
            context['per_page'] = data['per_page']
            context['page'] = data['page']
            context['total_pages'] = data['total_pages']
        pagination_list = generate_pagination_list(context['page'], context['total_pages'])
        context['pagination_list'] = pagination_list
        return render(request, 'users.html', context)
    
    
    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            self.cleaned_data = registration_form.cleaned_data
            if not self.validate_unique_users():
                return render(request, 'user_dynamic_form.html',
                      self.format_resp(
                          form=registration_form,
                          error_messages=self.error_messages
                      ))
            if self.register_user():                
                return redirect("users")

        return render(request, 'user_dynamic_form.html', 
                      self.format_resp(
                          form=registration_form,
                          error_messages=self.error_messages
                      ))
    
    def patch(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        json_data = request.body
        data = json_parser(json_data)
        st = [f"{key}='{value}'" for key, value in data.items()]
        value_updating = ','.join(st)
        query = "UPDATE misadmin_user SET " + value_updating + f" WHERE id={identifier} "

        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})
    

    def delete(self, request, *args, **kwargs):
        id = int(kwargs.get('id'))
        query = f"DELETE FROM misadmin_user WHERE id={id}"
        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})        


class ArtistsView(GenericListView):
    
    def get(self, request, *args, **kwargs):
        if kwargs:
            identifier = kwargs['identifier']            
            try:
                identifier = int(identifier)
                with DatabaseConnection() as db:
                    artist = db.get_by_id('misadmin_artist', identifier)                    
                artist_form = ArtistForm(artist)
                return render(request, 'artist_dynamic_form.html', {
                    'form': artist_form,
                    'current_page': 'Edit Artist',
                    'form_title': 'Update Artist',
                    'request_method': 'patch',
                    'artist_id': identifier
                })

            except:
                ...

            if identifier == 'add':
                return render(request, 'artist_dynamic_form.html', {
                    'form': ArtistForm(),
                    'current_page': 'Add Artist',
                    'form_title': 'Create Artist',
                })
        selected_page = request.GET.get('page')
        try:
            selected_page = int(selected_page)
        except:
            selected_page = None
        context = {}
        with DatabaseConnection() as db:
            data = db.execute_paginate_query("misadmin_artist", per_page=3, page=selected_page)
            context['artists'] = data['datas']
            context['per_page'] = data['per_page']
            context['page'] = data['page']
            context['total_pages'] = data['total_pages']
        pagination_list = generate_pagination_list(context['page'], context['total_pages'])
        context['pagination_list'] = pagination_list
        return render(request, 'artists.html', context)
    
    
    def post(self, request, *args, **kwargs):
        artist_form = ArtistForm(request.POST)
        if artist_form.is_valid():
            cleaned_data = artist_form.cleaned_data
            current_date = datetime.now()
            cleaned_data['created_at'] = current_date
            cleaned_data['updated_at'] = current_date
            keys = [f"{key}" for key, _ in cleaned_data.items()]
            values = [f"'{value}'" for _, value in cleaned_data.items()]
            str_keys = ','.join(keys)
            str_values = ','.join(values)
            query = f"INSERT INTO misadmin_artist({str_keys}) VALUES({str_values})"
            with DatabaseConnection() as db:
                db.execute_query(query)
                db.commit()
            return redirect("artists")
        return render(request, 'artist_dynamic_form.html', 
                      self.format_resp(
                          form=artist_form
                      ))
    
    def patch(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        json_data = request.body
        data = json_parser(json_data)
        st = [f"{key}='{value}'" for key, value in data.items()]
        value_updating = ','.join(st)
        query = "UPDATE misadmin_artist SET " + value_updating + f" WHERE id={identifier} "

        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})
    

    def delete(self, request, *args, **kwargs):
        id = int(kwargs.get('id'))
        query = f"DELETE FROM misadmin_artist WHERE id={id}"
        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})  
    
    
class ArtistMusicView(GenericListView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        query = f"SELECT * FROM misadmin_music WHERE artist_id_id={id}"
        data = {}
        with DatabaseConnection() as db:
            db.execute_query(query)
            data = db.filter_query()
        return render(request, 'music.html',
                      self.format_resp(
                          musics=data,
                          artist_id=id
                      ))
    

class MusicView(GenericListView):

    def get(self, request, *args, **kwargs):
        if kwargs:
            identifier = kwargs['identifier']   
            edit = False         
            try:
                identifier = int(identifier)
                edit = True
            except:
                edit = False
            
            if edit:
                with DatabaseConnection() as db:
                    music = db.get_by_id('misadmin_music', identifier)                    
                    music_form = MusicForm(music)
                    return render(request, 'music_dynamic_form.html', {
                        'form': music_form,
                        'current_page': 'Edit Music',
                        'form_title': 'Update Music',
                        'request_method': 'patch',
                        'music_id': identifier,
                        'artist_id': kwargs.get('artist_id')
                    })

            return render(request, 'music_dynamic_form.html', {
                'form': MusicForm(),
                'current_page': 'Add Music',
                'form_title': 'Create Music',
            })
                
    
    def post(self, request, *args, **kwargs):
        music_form = MusicForm(request.POST)
        if music_form.is_valid():
            cleaned_data = music_form.cleaned_data
            current_date = datetime.now()
            cleaned_data['created_at'] = current_date
            cleaned_data['updated_at'] = current_date
            keys = [f"{key}" for key, _ in cleaned_data.items()]
            values = [f"'{value}'" for _, value in cleaned_data.items()]
            str_keys = ','.join(keys) + ',artist_id_id'
            str_values = ','.join(values) + f",{kwargs.get('artist_id', ' ')}"
            query = f"INSERT INTO misadmin_music({str_keys}) VALUES({str_values})"
            with DatabaseConnection() as db:
                db.execute_query(query)
                db.commit()
            artist_id= kwargs.get('artist_id')       
            
            return HttpResponseRedirect(reverse('music', args=(artist_id,))) 
        return render(request, 'music_dynamic_form.html', 
                      self.format_resp(
                          form=music_form
                      ))
    
    def patch(self, request, *args, **kwargs):
        identifier = kwargs.get('identifier')
        json_data = request.body
        data = json_parser(json_data)
        st = [f"{key}='{value}'" for key, value in data.items()]
        value_updating = ','.join(st)
        query = "UPDATE misadmin_music SET " + value_updating + f" WHERE id={identifier} "

        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})
    

    def delete(self, request, *args, **kwargs):
        id = int(kwargs.get('id'))
        query = f"DELETE FROM misadmin_music WHERE id={id}"
        with DatabaseConnection() as db:
            db.execute_query(query)
            db.commit()
        return JsonResponse({'success': 'True'})  
    

def logout_user(request):
    logout(request)
    return redirect('login')

def index(request):
    return redirect('dashboard')