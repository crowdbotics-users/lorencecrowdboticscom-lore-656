from django import forms
# from django.utils.translation import ugettext_lazy as _

from .models import Task, Todo


class CustomerTaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('customer', 'tasker', 'status',)


class CustomerTodoCreationForm(forms.ModelForm):

    class Meta:
        model = Todo
        exclude = ('task',)
