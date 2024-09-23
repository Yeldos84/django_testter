from django import forms
from . models import ProfilePhoto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Question




class TestterUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(TestterUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        self.fields['email'].widget.attrs['placeholder'] = 'Адрес электронной почты'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтверждение пароля'

class TestterAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(TestterAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Логин'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'

class TestterPasswordResetForm(PasswordResetForm):
    pass


class TestterSetPasswordForm(SetPasswordForm):
    pass


class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(label='Select photo', required=False)

    class Meta:
        model = ProfilePhoto
        fields = ['photo']



