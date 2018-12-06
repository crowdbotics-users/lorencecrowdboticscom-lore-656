import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import OPTIONAL, TimeStampedModel
from core.utils import get_images_upload_path


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    STATUS_PENDING = 1
    STATUS_ACCEPTED = 2
    STATUS_IN_PROGRESS = 3
    STATUS_DONE = 4
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        'tasks.Category',
        verbose_name=_('Category'),
        related_name='tasks',
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        'users.User',
        verbose_name=_('Customer'),
        related_name='tasks',
        on_delete=models.CASCADE
    )
    tasker = models.ForeignKey(
        'users.User',
        verbose_name=_('Tasker'),
        related_name='customer_tasks',
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        _('Status'), choices=STATUS_CHOICES, default=STATUS_PENDING)
    start_date = models.DateTimeField(_('Start Date'))
    address = models.CharField(_('Address'), max_length=255)
    notes = models.TextField(_('Notes'), **OPTIONAL)

    class Meta:
        verbose_name = _('Tasks')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name


class Todo(TimeStampedModel):
    task = models.ForeignKey(
        'tasks.Task',
        verbose_name=_('Task'),
        related_name='todos',
        on_delete=models.CASCADE
    )
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = _('Todo')
        verbose_name_plural = _('Todos')

    def __str__(self):
        return self.name


class TodoImage(models.Model):
    todo = models.ForeignKey(
        'tasks.Todo',
        verbose_name=_('Todo'),
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(_('Image'), upload_to=get_images_upload_path)

    class Meta:
        verbose_name = _('Todo Image')
        verbose_name_plural = _('Todo Images')

    def __str__(self):
        return self.image.url
