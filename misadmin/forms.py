from django import forms
from generic.choices import GENDER, GENRE
from generic.utils import number_validator
from .models import Artist

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    phone = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Number'}))
    dob = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    gender = forms.ChoiceField(choices=GENDER)
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Address'}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        valid = number_validator(phone)
        if not valid:
            raise ValidationError(_("Please enter a valid number"))
        return phone        


class ArtistForm(forms.Form):
    name = forms.CharField(max_length=255)
    dob = forms.DateField()
    gender = forms.ChoiceField(choices=GENDER)
    address = forms.CharField(max_length=255)
    first_release_year = forms.CharField()
    no_of_albums_released = forms.IntegerField()


class MusicForm(forms.Form):
    artist_id = forms.ModelChoiceField(queryset=Artist.objects.all())
    title = forms.CharField(max_length=255)
    album_name = forms.CharField(max_length=255)
    genre = forms.ChoiceField(choices=GENRE)