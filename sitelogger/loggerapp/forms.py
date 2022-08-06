from django import forms
from django.contrib.auth.forms import AuthenticationForm


class ShortMyLink(forms.Form):
    redirect = forms.CharField(max_length=100, label='Редирект', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    screamer = forms.BooleanField(label='Скример?', required=False)
    name = forms.CharField(disabled=True ,required=False, max_length=30, label='Кастомная ссылка', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Необязательно (Доступно в PRO)'
               }

    ))


class ShortMyLinkPro(ShortMyLink):
    name = forms.CharField(empty_value='None',required=False, max_length=30, label='Кастомная ссылка', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Необязательно'
               }
    ))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ник', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    error_messages = {
        'invalid_login': (
            "Некорректный пароль"
        ),
        'inactive': "Ваш аккаунт заблокирован!",
    }
