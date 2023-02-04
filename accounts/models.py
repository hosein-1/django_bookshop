from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from random import choice


def set_default_avatar():
    # Returns a random avatar image.
    avatars = (
        'avatar1.jpg',
        'avatar2.jpg',
    )
    return choice(avatars)


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        _('Avatar'),
        upload_to='accounts/avatars/',
        default=f'accounts/default_avatars/{set_default_avatar()}')

    bio = models.TextField(_('Biography'), blank=True)


