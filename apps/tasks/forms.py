from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _

from .models import (
    Application,
    Task,
    Todo,
    TodoImage,
)


User = get_user_model()


class TaskForm(forms.ModelForm):
    date = forms.DateField(
        label=_('Date'), widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(
        label=_('Time'), widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Task
        exclude = ('customer', 'tasker', 'status', 'start_date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.todo_formset = TodoFormSet()
        self.initial = kwargs.get('initial')

    def clean(self):
        super().clean()
        self.todo_formset = TodoFormSet(self.data, self.files)

        if not self.todo_formset.is_valid():
            if self.todo_formset.non_form_errors():
                raise forms.ValidationError(
                    self.todo_formset.non_form_errors()[0])
            raise forms.ValidationError(
                _('Please check your todo task list errors below.'))

        return self.cleaned_data

    def save(self, *args, **kwargs):
        task = super().save(commit=False)
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')

        try:
            task.customer
        except User.DoesNotExist:
            task.customer = self.initial.get('customer')

        task.start_date = datetime.combine(date, time)
        task.save()

        # save formset
        for form in self.todo_formset.forms:
            if form.is_valid() and form.cleaned_data:
                form.initial['task'] = task
                form.save()

        return task


class TodoForm(forms.ModelForm):
    images = forms.ImageField(
        label=_('Images'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Todo
        exclude = ('task',)

    def save(self, *args, **kwargs):
        todo = super().save(commit=False)
        todo.task = self.initial.get('task')
        todo.save()

        try:
            images = self.files.getlist(f'{self.prefix}-images')
            for image in images:
                TodoImage.objects.create(
                    todo=todo,
                    image=image
                )
        except AttributeError:
            pass

        return todo


TodoFormSet = formset_factory(TodoForm, extra=1)


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('task',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = kwargs.get('initial')

    def save(self, *args, **kwargs):
        application = super().save(commit=False)
        application.tasker = self.initial.get('user')
        application.save()

        return application


class TaskStatusUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('status',)
