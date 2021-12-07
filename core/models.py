from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and _ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    display_name = models.CharField(max_length=100, null=True, blank=True,
                                    help_text='Alternate name')

    REQUIRED_FIELDS = ['email', 'first_name', ]
    objects = UserManager()

    def __str__(self):
        if self.display_name:
            return self.display_name
        return self.get_full_name()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        If the user has specified the display name, it will be returned.
        """
        if self.display_name:
            return self.display_name
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Category(models.Model):
    category = models.CharField(max_length=50, null=False, blank=False, help_text='Category of the book')
