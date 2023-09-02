from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

class Registration(UserCreationForm):
    first_name = forms.CharField(label= ("First Name"))
    last_name = forms.CharField(label= ("Last Name"))
    username = forms.EmailField(label=("E-mail")) 
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2')
        