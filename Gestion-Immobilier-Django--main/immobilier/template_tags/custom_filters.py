## immobilier_app/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """Ajoute une classe CSS aux widgets de formulaire"""
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': arg})
    return value
