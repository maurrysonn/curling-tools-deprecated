# -*- coding: utf-8 -*-
from django.conf import settings
# Django Generic Views
from django.views.generic import TemplateView
from django.views.generic.list import ListView


class CTModelContextMixin(object):

    def get_context_data(self, **kwargs):
        model_data = {}
        if self.model:
            model_data['app_label'] = self.model._meta.app_label
            model_data['verbose_name'] = self.model._meta.verbose_name
            model_data['verbose_name_plural'] = self.model._meta.verbose_name_plural
        # Updating context
        context = super(CTModelContextMixin, self).get_context_data(**kwargs)
        context.update(model_data)
        return context


class CTSubmenuMixin(object):
    
    snippet_submenu = None
    submenu_items = ()

    def get_snippet_submenu(self):
        if self.snippet_submenu:
            return self.snippet_submenu
        return settings.DEFAULT_SNIPPET_SUBMENU

    def get_submenu_items(self):
        return self.submenu_items

    def get_context_data(self, **kwargs):
        context = super(CTSubmenuMixin, self).get_context_data(**kwargs)
        submenu_items = []
        # Generating submenu items
        for item in self.get_submenu_items():
            submenu_items.append({'title': item[0],
                                  'links': [ {'title': link[0], 'url': link[1]}
                                             for link in item[1]]})
        # Add submenu into context
        if submenu_items:
            submenu = {'items': submenu_items,
                       'snippet': self.get_snippet_submenu()}
            context[settings.CONTEXT_SUBMENU] = submenu
        return context


class CTModelListMixin(CTModelContextMixin):
    
    snippet_model_list = None
    
    def get_snippet_model_list(self):
        snippet_list = []
        if self.snippet_model_list:
            return self.snippet_model_list
        return settings.DEFAULT_SNIPPET_MODEL_LIST
    
    def get_context_data(self, **kwargs):
        context = super(CTModelListMixin, self).get_context_data(**kwargs)
        print "CONTEXT :", context
        # Add snippet template infos will be included
        context[settings.CONTEXT_MODEL_LIST] = {'snippet': self.get_snippet_model_list()}
        return context


# ---------------
# Base Views
# ---------------

class CTTemplateView(CTSubmenuMixin, TemplateView): pass
class CTListView(CTSubmenuMixin, CTModelListMixin, ListView):
    template_name = 'core/model_list.html'
    list_display = ()
    list_display_links = ()
