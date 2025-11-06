from django import template
register = template.Library()

@register.filter
def enumerate(value):
    return enumerate(value)
