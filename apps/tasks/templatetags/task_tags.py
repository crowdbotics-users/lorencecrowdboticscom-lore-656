from django.template import Library

register = Library()


@register.filter
def has_rated(user, task):
    return task.has_rated_by(user)
