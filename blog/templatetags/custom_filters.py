from django import template

register = template.Library()


@register.filter
def first_sentence(value):
    if not isinstance(value, str):
        return ""
    return value.split(".")[0] + "." if "." in value else value
