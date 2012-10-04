# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
# Django Generic Views
from django.views.generic import TemplateView
from django.views.generic.list import ListView


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


class CTModelListMixin(object):
    
    snippet_model_list = None
    
    def get_snippet_model_list(self):
        snippet_list = []
        if self.snippet_model_list:
            return self.snippet_model_list
        return settings.DEFAULT_SNIPPET_MODEL_LIST
    
    def get_context_data(self, **kwargs):
        context = super(CTModelListMixin, self).get_context_data(**kwargs)
        # Add snippet template infos will be included
        context[settings.CONTEXT_MODEL_LIST] = {'snippet': self.get_snippet_model_list()}
        return context


# ---------------
# Base Views
# ---------------

class CTTemplateView(CTSubmenuMixin, TemplateView): pass
class CTListView(CTSubmenuMixin, CTModelListMixin, ListView): pass


# ---------------
# TESTS Views
# ---------------

class TestSubmenu(CTSubmenuMixin):
    "Define a submenu for a module."
    submenu_items = (
        ('Global Menu', (('Item #1', reverse_lazy('test-view')),
                         ('Item #2', reverse_lazy('test-view')))),
        ('Other Submenu', (('Other Item #1', reverse_lazy('test-view-2')),
                           ('Ohther Item #2', reverse_lazy('test-view-2'))))
        )
    
class TestView(TestSubmenu, CTTemplateView):
    "Simple template view"
    template_name = 'core/test/test_view.html'

    
class TestListView(CTModelListMixin, TestSubmenu, TemplateView):
    template_name = 'core/model_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(TestListView, self).get_context_data(**kwargs)
        # Add object list like MultipleObjectMixin
        context['object_list'] = range(25)
        print "CONTEXT =", context
        return context
