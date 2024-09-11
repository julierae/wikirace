from django import template
from django.template.defaultfilters import stringfilter

from wikirace.models import WIKIPEDIA_URL

register = template.Library()


@register.filter
@stringfilter
def to_wiki_link(value):
    if not value:
        return ''
    return f"{WIKIPEDIA_URL}{value.replace(' ', '_')}"


@register.filter
@stringfilter
def to_wiki_title(value):
    if not value:
        return ''
    return value.replace("_", " ").replace("%20", " ").replace("-", " ")
