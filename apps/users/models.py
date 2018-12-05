from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    TYPE_TASKER = 1
    TYPE_CUSTOMER = 2
    USER_TYPE_CHOICES = (
        (TYPE_TASKER, 'Tasker'),
        (TYPE_CUSTOMER, 'Customer'),
    )

    contact = models.CharField(_('Contact No.'), max_length=20)
    type = models.IntegerField(_('Type'), choices=USER_TYPE_CHOICES, default=TYPE_TASKER)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_full_name()
