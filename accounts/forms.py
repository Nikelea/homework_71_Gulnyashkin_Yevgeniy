from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from accounts.models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', strip=False, required=True, widget=forms.PasswordInput)
    email = forms.CharField(label="Электронная почта", required=True, widget=forms.EmailInput)

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError('Эта почта уже зарегестрированна')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password', 'password_confirm']
        labels = {'username': 'Username', 'email': 'Email*', 'first_name': 'Name'}


class ProfileRegistrationForm(forms.ModelForm):
    avatar = forms.FileField(required=True)

    class Meta:
        model = Profile
        fields = ['avatar', 'about', 'phone', 'sex']
        labels = {'avatar': 'Avatar', 'about': 'About', 'phone': 'Contact phone', 'sex': 'Sex'}
        SEX_CHOICES = (('Man', 'Woman'))
        sex = forms.ChoiceField(
            widget=forms.Select(choices=SEX_CHOICES)
    )
