from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from .models import Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ("email", "password1", "password2", 'first_name', 'last_name', 'birth')
