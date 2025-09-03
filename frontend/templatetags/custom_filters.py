import re
from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def as_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def slugify_fr(value):
    """
    Converts to ASCII, converts spaces to hyphens, removes characters that aren't
    alphanumerics, underscores, or hyphens, and converts to lowercase.
    Also handles French specific characters.
    """
    value = str(value)
    value = re.sub(r'[àáâãäå]', 'a', value)
    value = re.sub(r'[èéêë]', 'e', value)
    value = re.sub(r'[ìíîï]', 'i', value)
    value = re.sub(r'[òóôõö]', 'o', value)
    value = re.sub(r'[ùúûü]', 'u', value)
    value = re.sub(r'[ç]', 'c', value)
    value = re.sub(r'[ñ]', 'n', value)
    return slugify(value)