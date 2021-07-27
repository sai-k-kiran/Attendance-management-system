from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class registerForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ['username', 'email', 'password1', 'password2']

class statusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['status']