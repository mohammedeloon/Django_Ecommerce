from django import template

register = template.Library()

@register.filter(name='slugify')
def slugify(value):
    return value.replace(' ', '-')