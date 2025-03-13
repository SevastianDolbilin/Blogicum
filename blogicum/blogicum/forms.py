from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text="Не обязательно.", label="Имя"
    )
    last_name = forms.CharField(
        max_length=30, required=False,
        help_text="Не обязательно.",
        label="Фамилия"
    )
    email = forms.EmailField(
        required=True,
        help_text="Введите ваш адрес электронной почты.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
