from django import forms
from .models import Coffee

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'description', 'price', 'photo', 'exist']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'floatingInput',
                    'placeholder': "Название напитка",
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Описание напитка",
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Цена напитка",
                }
            ),
            'photo': forms.FileInput(
                attrs={
                    'class': "form-control",
                    'type': "file",
                    'id': "formFile",
                    'placeholder': "Фотография",
                }),
        }


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 11, })
    )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2,
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Введите логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=2,
    )
    password = forms.CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
