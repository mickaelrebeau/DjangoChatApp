from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import *


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.is_avtive = True
            user.save()
        
        return user
