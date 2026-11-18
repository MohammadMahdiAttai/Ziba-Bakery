from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'suburb', 'postcode']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'suburb': forms.TextInput(attrs={'placeholder': 'Suburb'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
        }
