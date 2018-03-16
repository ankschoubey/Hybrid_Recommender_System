from django import template

register = template.Library()

@register.filter(is_safe=True)
def hash(h, key):
    return h[key]
