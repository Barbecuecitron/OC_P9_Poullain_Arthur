from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur", label_suffix="", max_length=63)
    username.widget.attrs.update({'class': 'charfield'})

    password = forms.CharField(
        label="Mot de passe", label_suffix="",
        max_length=63, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'charfield'})


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']
