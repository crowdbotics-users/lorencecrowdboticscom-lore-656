from django.contrib.auth import get_user_model
from django.views.generic import (
    DetailView,
)


User = get_user_model()


class ProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/profile.html'
