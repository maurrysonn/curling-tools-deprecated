# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json

from curling_tools.core.forms import CTModelForm
# Generic Curling Tools views
from curling_tools.core.views import (CTListView,
                                      CTDetailView,
                                      CTUpdateView,
                                      CTCreateView,
                                      CTDeleteView)

# --------------------------
# JSON rendering methods
# --------------------------

def render_json_response(**kwargs):
    # Code Response default : 200
    if 'code_response' not in kwargs:
        kwargs['code_response'] = 200
    return HttpResponse(json.dumps(kwargs),
                        content_type='application/json')

def render_json_response_500(**kwargs):
    # Default Code Response = 500
    if 'code_response' not in kwargs:
        kwargs['code_response'] = 500
    # Default Msg
    if 'msg' not in kwargs:
        kwargs['msg'] = _(u"An error has occured during the request.")
    # Return a json response
    return render_json_response(**kwargs)

# ---------------
# URLs Tools
# ---------------

def get_default_model_url(model,
                          submenu_mixin=None,
                          form_class=None,
                          url_name=None,
                          prefix_pattern='',
                          prefix_name='',
                          list_view=CTListView,
                          detail_view=CTDetailView,
                          creation_view=CTCreateView,
                          update_view=CTUpdateView,
                          delete_view=CTDeleteView):

    module_name = model._meta.module_name
    # Get default FormClass for model
    if not form_class:
        form_class = model_forms.modelform_factory(model, CTModelForm)
    # Get default URL name
    if not url_name:
        url_name = module_name
    # Generation of urlpatterns
    urlpatterns = patterns('')
    # Kargs of Views
    view_kwargs = {}
    if submenu_mixin:
        view_kwargs['submenu_items'] = submenu_mixin.submenu_items
    # List View
    if list_view:
        list_view_instance = list_view.as_view(model=model, **view_kwargs)
        urlpatterns += patterns('',
                               url(r'^%s%s/$' % (prefix_pattern, module_name),
                                   list_view_instance,
                                   name='%s%s%s' % (prefix_name, url_name, settings.URL_LIST_SUFFIX)))
    # Detail View
    if detail_view:
        urlpatterns += patterns('',
                               url(r'^%s%s/(?P<pk>\d+)/$' % (prefix_pattern, module_name),
                                   detail_view.as_view(model=model, **view_kwargs),
                                   name="%s%s%s" % (prefix_name, url_name, settings.URL_DETAIL_SUFFIX)))

    # Add View
    if creation_view:
        # First, get form class define in view
        view_form_class = getattr(creation_view, 'form_class', None)
        # Then, get form class parameter or generic model form
        if not view_form_class:
            view_form_class = form_class
        urlpatterns += patterns('',
                                url(r'^%s%s/add/$' % (prefix_pattern, module_name),
                                    creation_view.as_view(model=model, form_class=view_form_class, **view_kwargs),
                                    name="%s%s%s" % (prefix_name, url_name, settings.URL_ADD_SUFFIX)))
    # Update View
    if update_view:
        # First, get form class define in view
        view_form_class = getattr(update_view, 'form_class', None)
        # Then, get form class parameter or generic model form
        if not view_form_class:
            view_form_class = form_class
        urlpatterns += patterns('',
                                url(r'^%s%s/(?P<pk>\d+)/edit/$' % (prefix_pattern, module_name),
                                   update_view.as_view(model=model, form_class=view_form_class, **view_kwargs),
                                   name="%s%s%s" % (prefix_name, url_name, settings.URL_EDIT_SUFFIX)))
    # Delete View
    if delete_view:
        urlpatterns += patterns('',
                               url(r'^%s%s/(?P<pk>\d+)/delete/$' % (prefix_pattern, module_name),
                                   delete_view.as_view(model=model, **view_kwargs),
                                   name="%s%s%s" % (prefix_name, url_name, settings.URL_DELETE_SUFFIX)))

    return urlpatterns
