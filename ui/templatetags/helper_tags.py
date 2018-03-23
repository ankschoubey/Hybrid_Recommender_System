from django import template

register = template.Library()

@register.filter(is_safe=True)
def hash(h, key):
    return h[key]

@register.filter(is_safe=True)
def join_list(items):
    items = [str(i) for i in items]
    return ', '.join(items)
