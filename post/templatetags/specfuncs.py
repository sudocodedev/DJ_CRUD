# special tags for django template
from django import template

register = template.Library()

@register.filter(name="tagSplit",is_safe=True)
def splitString(s:str,delimiter:str) -> list:
    l=list(s.strip().split(delimiter))
    return l

@register.filter(name="AddClass",is_safe=True)
def addClassToHTML(value,arg):
    return value.as_widget(attrs={'class':arg})

@register.filter(name="AddPlaceholder",is_safe=True)
def addPlaceholderToHTML(value,arg):
    return value.as_widget(attrs={'placeholder':arg})
