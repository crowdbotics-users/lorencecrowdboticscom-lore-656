from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import (
    Application,
    Task,
)
from .forms import (
    AcceptTaskerForm,
    ApplicationForm,
    TaskForm,
    TaskStatusUpdateForm,
)
from apps.users.forms import RatingForm
from apps.users.models import Rating


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        user = self.request.user

        queryset = user.tasks.all()
        if user.type == user.TYPE_TASKER:
            queryset = user.customer_tasks.all()

        return queryset.order_by('status')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = RatingForm(initial={'user': self.request.user})
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class AvailableTaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/available_task_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.type == user.TYPE_TASKER:
            applied_tasks = [application.task.id for application in user.applications.all()]
            return Task.objects\
                .filter(status=Task.STATUS_PENDING)\
                .exclude(id__in=applied_tasks)

        return HttpResponseNotFound('<h1>Page not found</h1>')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_manage.html'
    success_url = reverse_lazy('tasks:task-list')

    def get_initial(self):
        return {'customer': self.request.user}


class TaskApplyView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'tasks/task_apply.html'
    success_url = reverse_lazy('tasks:available-task-list')

    def get_initial(self):
        return {'user': self.request.user}


class TaskRatingView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'tasks/rating.html'
    success_url = reverse_lazy('tasks:task-list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('tasks:task-list'))

    def get_initial(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))

        return {
            'user': self.request.user,
            'task': task,
        }


class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    form_class = TaskStatusUpdateForm
    success_url = reverse_lazy('tasks:task-list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('tasks:task-list'))


class AcceptTaskerView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task'
    form_class = AcceptTaskerForm
    success_url = reverse_lazy('tasks:task-list')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('tasks:task-detail', args=(self.kwargs.get('pk'),))
