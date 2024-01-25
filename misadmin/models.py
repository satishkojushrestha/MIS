from django.db import models
from django.contrib.auth.models import AbstractUser
from generic.choices import GENDER, GENRE
from datetime import datetime

class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=False)
    email = models.CharField(max_length=255, null=True, blank=False)
    password = models.CharField(max_length=255, null=True, blank=False)
    phone = models.CharField(max_length=255, null=True, blank=False)
    dob = models.DateField(null=True, blank=False)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)


class Artist(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    dob = models.DateField(null=True, blank=False)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    first_release_year = models.CharField(max_length=5, null=True, blank=False)
    no_of_albums_released = models.IntegerField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Music(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=False)
    title = models.CharField(max_length=255, null=True, blank=False)
    album_name = models.CharField(max_length=255, null=True, blank=False)
    genre = models.CharField(choices=GENRE, max_length=10, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)