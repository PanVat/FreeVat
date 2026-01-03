import os
from django import template

register = template.Library()

# Vrátí pouze jméno souboru, ne celou cestu
@register.filter
def basename(value):
    if not value:
        return ""
    return os.path.basename(str(value))