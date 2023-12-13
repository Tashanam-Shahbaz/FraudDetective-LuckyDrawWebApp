from django import template

register = template.Library()

@register.filter
def field_display_value(user, field_name):
    if hasattr(user, field_name):
        return getattr(user, field_name)
    return ''