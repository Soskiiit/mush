from django import forms
from django.forms.widgets import EmailInput, PasswordInput

from .models import User


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Введённые пароли не совпадают')

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'На эту почту уже зарегистрирован аккаунт'
            )

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': 'form-control'})
    )


class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    nickname = forms.CharField(max_length=100)
    bio = forms.CharField(max_length=256)
    twitter = forms.CharField(max_length=100)
    github = forms.CharField(max_length=100)
