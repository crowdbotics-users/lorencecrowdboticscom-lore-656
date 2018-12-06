from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.TaskListView.as_view(),
        name='task-list'
    ),
    url(
        regex=r'^create/$',
        view=views.TaskCreateView.as_view(),
        name='task-create'
    ),
]
