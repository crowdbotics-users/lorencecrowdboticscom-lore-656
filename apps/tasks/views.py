from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import (
    CreateView,
    ListView,
)

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.type == user.TYPE_TASKER:
            return user.customer_tasks.all()

        return user.tasks.all()


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_manage.html'
    success_url = reverse_lazy('tasks:customer-task-list')

    def get_initial(self):
        return {'customer': self.request.user}
