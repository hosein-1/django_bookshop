from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import AbstractUser
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = AbstractUser
        fields = ('username', 'email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AbstractUser
        fields = ('username', 'email', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'username', 'email', 'bio', 'first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
