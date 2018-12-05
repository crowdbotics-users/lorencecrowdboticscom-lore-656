from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm


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
