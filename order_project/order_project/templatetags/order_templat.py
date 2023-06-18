from django import template

register = template.Library()

@register.filter
def minimize_desc(value):
    if len(value) > 20:
        return value[:20] + "..."
    return value