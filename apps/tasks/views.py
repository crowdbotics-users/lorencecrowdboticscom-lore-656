from django.views.generic.base import TemplateView

from .models import Task
from .forms import CustomerTaskCreationForm, CustomerTodoCreationForm


class TaskerDashboardView(TemplateView):

    template_name = "tasks/tasker_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_tasks'] = Task.objects.filter(tasker=None,
                                                         status=Task.STATUS_PENDING)
        context['my_tasks'] = Task.objects.filter(tasker=self.request.user)
        return context


class CustomerDashboardView(TemplateView):

    template_name = "tasks/customer_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_tasks'] = Task.objects.filter(customer=self.request.user)
        context['task_form'] = CustomerTaskCreationForm()
        context['todo_form'] = CustomerTodoCreationForm()

        return context
