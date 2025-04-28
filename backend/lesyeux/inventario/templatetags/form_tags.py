from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """Añade una clase CSS al valor"""
    return value.as_widget(attrs={'class': arg})
