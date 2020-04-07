from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class RegistrationFormUniqueEmail(forms.ModelForm):
    """ Registration form """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "email")
        labels = ('Имя пользователя', "Ваше имя и фамилия", "Адрес электронной почты")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return cd["password2"]


class LoginForm(forms.Form):
    """ Login form """
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    """ Edit user-db form """
    class Meta:
        model = User
        fields = ("first_name", "email")


class ProfileEditForm(forms.ModelForm):
    """ Edit progile-db form """
    class Meta:
        model = Profile
        fields = ("birthdate",)
        labels = {
            "birthdate": 'Дата рождения'
        }
