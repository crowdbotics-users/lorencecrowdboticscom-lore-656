import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_images_upload_path(instance, filename):
    return os.path.join(
        'media',
        'images',
        instance.__class__.__name__.lower(),
        filename
    )


def send_email_template(request, subject, template, recipients, data=None):
    """
    This function sends an email using a selected template.

    Arguments:
        subject: the subject of the email
        template: the template to be used for the email
        recipient: a list of recipients the email will be sent to
        data: a dictionary to be added as context variables in the email
    """
    context = {
        'current_site': Site.objects.get_current(),
        'protocol': 'https' if request.is_secure() else 'http'
    }
    context.update(data)

    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)

    send_mail(
        subject=f'[Site.objects.get_current().name] {subject}',
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
        html_message=html_content
    )
