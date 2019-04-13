from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm, UserChangeForm as ChangeForm
from .models import User


class UserCreationForm(CreationForm):
    class Meta(CreationForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'address')


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'address')
