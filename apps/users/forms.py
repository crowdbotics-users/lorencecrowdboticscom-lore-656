from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm

from apps.users.models import Rating


User = get_user_model()


class SignupForm(SignupForm):

    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    contact = forms.CharField(label=_('Contact No.'), max_length=30)
    type = forms.ChoiceField(label=_('Type'), choices=User.USER_TYPE_CHOICES)

    def save(self, request):
        user = super().save(request)
        user.contact = self.cleaned_data.get('contact')
        user.type = self.cleaned_data.get('type')
        user.save()
        return user


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('rate', 'remarks',)
        widgets = {
            'rate': forms.NumberInput(attrs={'class': 'rating d-none'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = kwargs.get('initial')

    def save(self, *args, **kwargs):
        rating = super().save(commit=False)
        task = self.initial.get('task')
        user = self.initial.get('user')

        if user.type == user.TYPE_TASKER:
            receiver = task.customer
            sender = task.tasker
        else:
            receiver = task.tasker
            sender = task.customer

        rating.task = self.initial.get('task')
        rating.receiver = receiver
        rating.sender = sender
        rating.save()

        return rating
