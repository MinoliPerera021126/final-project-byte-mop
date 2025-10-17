from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=(('admin', 'System Admin'), ('ma', 'Management Assistant')))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
