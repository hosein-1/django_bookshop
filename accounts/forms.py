from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AbstractUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = AbstractUser
        fields = ('username', 'email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AbstractUser
        fields = ('username', 'email', )