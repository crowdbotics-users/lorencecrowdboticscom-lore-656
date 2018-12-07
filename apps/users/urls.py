from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^profile/(?P<pk>\d+)/$',
        view=views.ProfileView.as_view(),
        name='profile'
    ),
]
