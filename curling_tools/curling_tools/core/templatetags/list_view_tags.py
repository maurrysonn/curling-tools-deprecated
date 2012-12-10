# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django import template

register = template.Library()


@register.filter
def default_add_url(ct_model_infos):
    try:
        return reverse(u'%s:%s%s' % (ct_model_infos['app_label'], ct_model_infos['module_name'], settings.URL_ADD_SUFFIX))
    except:
        return ''


# ---------------------
# Change List Tags
# ---------------------

def get_cl_context(context):
    ct_model_list = context.get(settings.CONTEXT_MODEL_LIST, None)
    if ct_model_list:
        return ct_model_list.get('cl', None)
    return None


@register.inclusion_tag('core/snippets/headers_model_list_snippet.html',
                        takes_context=True)
def headers_list(context, cl=None):
    # Get Change List Infos Wrapper in context
    if cl is None:
        cl = get_cl_context(context)
    return {'cl': cl}


@register.inclusion_tag('core/snippets/items_model_list_snippet.html', takes_context=True)
def item_list(context, cl=None, obj=None):
    if cl is None:
        cl = get_cl_context(context)
    if obj is None:
        obj = context.get('object', None)
    if cl and obj:
        return {'items': cl.items_for_obj(obj)}
    return {}
