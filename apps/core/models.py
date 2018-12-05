from django.db import models
from django.utils.translation import ugettext_lazy as _


OPTIONAL = {
    'blank': True,
    'null': True,
}


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True
