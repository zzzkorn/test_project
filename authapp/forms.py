from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import RespondentUser


class RespondentUserLoginForm(AuthenticationForm):
    class Meta:
        model = RespondentUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwarg):
        super(RespondentUserLoginForm, self).__init__(*args, **kwarg)
        # Для красивого отображения формы (bootstrap)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RespondentUserRegisterForm(UserCreationForm):
    class Meta:
        model = RespondentUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'age', 'avatar')

    def __init__(self, *args, **kwarg):
        super(RespondentUserRegisterForm, self).__init__(*args, **kwarg)
        # Для красивого отображения формы (bootstrap)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RespondentUserChangeForm(UserChangeForm):
    class Meta:
        model = RespondentUser
        fields = ('username', 'first_name', 'last_name', 'age', 'avatar')

    def __init__(self, *args, **kwarg):
        super(RespondentUserChangeForm, self).__init__(*args, **kwarg)
        # Для красивого отображения формы (bootstrap)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()
