from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
)

from .models import Task
from .forms import TaskForm, TaskApplyForm
from ..users.forms import RatingForm
from ..users.models import Rating


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
    pk_url_kwarg = 'pk'

    def get_object(self):
        return Task.objects.get(pk=self.kwargs['pk'])


class AvailableTaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/available_task_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.type == user.TYPE_TASKER:
            return Task.objects.filter(tasker=None)

        return HttpResponseNotFound('<h1>Page not found</h1>')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    pk_url_kwarg = 'pk'

    def get_object(self):
        return Task.objects.get(pk=self.kwargs['pk'])


class AvailableTaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/available_task_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.type == user.TYPE_TASKER:
            return Task.objects.filter(tasker=None)

        return HttpResponseNotFound('<h1>Page not found</h1>')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_manage.html'
    success_url = reverse_lazy('tasks:task-list')

    def get_initial(self):
        return {'customer': self.request.user}


class TaskApplyView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = TaskApplyForm(data)
        task = data.get('task')

        if form.is_valid():
            return HttpResponseRedirect(reverse_lazy('tasks:task-list'))
        else:
            form = TaskApplyForm()

        return HttpResponseRedirect(
            reverse('tasks:task-detail', {'pk': task.id})
        )


class TaskRatingView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'tasks/rating.html'
    success_url = reverse_lazy('tasks:task-list')

    def get_initial(self):
        task = Task.objects.get(id=self.kwargs.get('pk'))

        return {
            'user': self.request.user,
            'task': task,
        }
