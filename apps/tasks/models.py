import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import OPTIONAL, TimeStampedModel
from apps.core.utils import get_images_upload_path


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
        on_delete=models.CASCADE,
        **OPTIONAL
    )
    status = models.IntegerField(
        _('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    cost = models.DecimalField(_('Cost'), max_digits=15, decimal_places=2)
    address = models.CharField(_('Address'), max_length=255)
    start_date = models.DateTimeField(_('Start Date'))
    notes = models.TextField(_('Notes'), **OPTIONAL)

    class Meta:
        verbose_name = _('Tasks')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return str(self.id)

    def has_rated_by(self, user):
        return self.ratings.filter(task=self, sender=user).exists()


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
        return str(self.task.id)


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


class Application(TimeStampedModel):
    task = models.ForeignKey(
        'tasks.Task',
        verbose_name=_('Task'),
        related_name='applications',
        on_delete=models.CASCADE
    )
    tasker = models.ForeignKey(
        'users.User',
        verbose_name=_('Tasker'),
        related_name='applications',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __str__(self):
        return self.tasker.get_full_name()
