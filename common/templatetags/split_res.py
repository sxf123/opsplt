from django import template

register = template.Library()

@register.filter(name='split_path')
def split_path(value):
    return value.split('/')