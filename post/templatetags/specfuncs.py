# special tags for django template
from django import template

register = template.Library()

@register.filter(name="tagSplit",is_safe=True)
def splitString(s:str,delimiter:str) -> list:
    l=list(s.strip().split(delimiter))
    return l
