from django import forms
from django.contrib.auth.models import User
from .models import Profile


class CreateMAForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'phone']
