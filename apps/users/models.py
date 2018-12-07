from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel, OPTIONAL
from core.utils import get_images_upload_path


class User(AbstractUser):
    TYPE_TASKER = 1
    TYPE_CUSTOMER = 2
    USER_TYPE_CHOICES = (
        (TYPE_TASKER, 'Tasker'),
        (TYPE_CUSTOMER, 'Customer'),
    )

    image = models.ImageField(_('Image'), upload_to=get_images_upload_path, **OPTIONAL)
    contact = models.CharField(_('Contact No.'), max_length=20)
    type = models.IntegerField(_('Type'), choices=USER_TYPE_CHOICES, default=TYPE_TASKER)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_full_name()

    @property
    def average_rating(self):
        return round(
            self.received_ratings.all()\
                .aggregate(average=Avg('rate'))\
                .get('average', 0)
        )

class Rating(TimeStampedModel):
    task = models.ForeignKey(
        'tasks.Task',
        verbose_name=_('Task'),
        related_name='ratings',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        'users.User',
        verbose_name=_('Sender'),
        related_name='sent_ratings',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        'users.User',
        verbose_name=_('Receiver'),
        related_name='received_ratings',
        on_delete=models.CASCADE
    )
    rate = models.PositiveIntegerField(_('Rate'))
    remarks = models.TextField(_('Remarks'))

    class Meta:
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')

    def __str__(self):
        return str(self.rate)
