from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.template.base import Library
from django.template.defaultfilters import stringfilter


register = Library()


@register.filter(is_safe=True)
@stringfilter
def escapeamps(value):
    """
    Escapes the ampersands in an HTML string.
    """
    return mark_safe(force_text(value).replace('&', '&amp;'))
