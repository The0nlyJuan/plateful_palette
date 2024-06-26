import re
from django import template

register = template.Library()

@register.filter(name='cookbook')
def wikibook_format(value):
    # Find all patterns like [[Cookbook:Cup|cup]] and replace them with just 'cup'
    return re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', value)

@register.filter(name='startswith')
def startswith(value, arg):
    """Checks if the value starts with the given argument."""
    return value.startswith(arg)

@register.filter(name='header')
def header(value):
    return value.replace("=", "")

@register.filter(name='ingredient')
def ingredient(value):
    return value.replace("*", "")

@register.filter(name='procedure')
def procedure(value):
    return value.replace('#', "")
