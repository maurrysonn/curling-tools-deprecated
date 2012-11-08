# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('base/snippets/address_snippet.html')
def html_address(address):
    return {'object': address}
