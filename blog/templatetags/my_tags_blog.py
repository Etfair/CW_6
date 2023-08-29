from django import template

register = template.Library()


@register.filter()
def mediapath(val):
    return f'/media/{val}'


