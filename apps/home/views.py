from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import RedirectView

from home.models import CustomText, HomePage


def home(request):
    packages = [
	{'name':'djangorestframework', 'url': 'http://pypi.python.org/pypi/djangorestframework/3.7.7'},
	{'name':'django-bootstrap4', 'url': 'http://pypi.python.org/pypi/django-bootstrap4/0.0.5'},
	{'name':'django-allauth', 'url': 'http://pypi.python.org/pypi/django-allauth/0.34.0'},
    ]
    context = {
        'customtext': CustomText.objects.first(),
        'homepage': HomePage.objects.first(),
        'packages': packages
    }
    return render(request, 'home/index.html', context)


class DashboardView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.type == user.TYPE_TASKER:
            return reverse_lazy('tasks:available-task-list')
        return reverse_lazy('tasks:task-create')
