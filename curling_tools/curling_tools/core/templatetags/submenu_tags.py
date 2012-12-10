# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def is_active_item(item, url):
    # url = context.get('request_url', None)
    # if url is not None:
    if url in [ link['url'] for link in item['links']]:
        return True
    return False
