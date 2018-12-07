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
    url(
        regex=r'^available/$',
        view=views.AvailableTaskListView.as_view(),
        name='available-task-list'
    ),
    url(
        regex=r'^(?P<pk>[-:\w]+)/$',
        view=views.TaskDetailView.as_view(),
        name='task-detail'
    ),
    url(
        regex=r'^(?P<pk>[-:\w]+)/apply/$',
        view=views.TaskApplyView.as_view(),
        name='task-apply'
    ),
    url(
        regex=r'^(?P<pk>[-:\w]+)/rate/$',
        view=views.TaskRatingView.as_view(),
        name='task-rate'
    ),
]
