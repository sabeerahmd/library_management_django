from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username=forms.CharField()
    email=forms.CharField()
    password1=forms.CharField()
    password2=forms.CharField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']