from django import template

register = template.Library()


# Funkce, která formátuje počet trojúhelníků a vrcholů (např. z 15200 -> 15,2k)
@register.filter
def format_numbers(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return str(value)

    elif value < 1_000_000:
        # Tisíce
        formatted = value / 1000.0
        if formatted.is_integer():
            return f"{int(formatted)}k"
        else:
            return f"{formatted:.1f}k".replace('.', ',')

    else:
        # Miliony
        formatted = value / 1_000_000.0
        if formatted.is_integer():
            return f"{int(formatted)}m"
        else:
            return f"{formatted:.1f}m".replace('.', ',')
