from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^tasker-dashboard/$',
        view=views.TaskerDashboardView.as_view(),
        name="tasker-dashboard"
    ),
    url(
        regex=r'^customer-dashboard/$',
        view=views.CustomerDashboardView.as_view(),
        name="customer-dashboard"
    ),
]
