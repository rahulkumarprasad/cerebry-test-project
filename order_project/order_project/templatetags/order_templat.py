from django import template

register = template.Library()

@register.filter
def minimize_desc(value):
    '''This is used for minimizing long text in html file'''
    if len(value) > 20:
        return value[:20] + "..."
    return value