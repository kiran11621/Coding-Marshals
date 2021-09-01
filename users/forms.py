from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
from dobwidget import DateOfBirthWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }


class InfoForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['gender', 'date_of_birth', 'country',
                  'city', 'college', 'mobile', 'profile_pic']
        widgets = {
            'date_of_birth': DateOfBirthWidget(),
        }
