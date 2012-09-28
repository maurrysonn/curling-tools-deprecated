# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy


class SubmenuMixin(object):
    
    template_submenu = None
    submenu_items = ()

    def get_template_submenu(self):
        if self.template_submenu:
            return self.template_submenu
        return settings.DEFAULT_SUBMENU_TEMPLATE

    def get_submenu_items(self):
        return self.submenu_items

    def get_context_data(self, **kwargs):
        context = super(SubmenuMixin, self).get_context_data(**kwargs)
        submenu_items = []
        # Generating submenu items
        for item in self.get_submenu_items():
            submenu_items.append({'title': item[0],
                                  'links': [ {'title': link[0], 'url': link[1]}
                                             for link in item[1]]})
        # Add submenu into context
        if submenu_items:
            submenu = {'items': submenu_items,
                       'template': self.get_template_submenu()}
            context['ct_submenu'] = submenu
        return context



class TestSubmenuMixin(SubmenuMixin):

    submenu_items = (
        ('Global Menu', (('Item #1', reverse_lazy('test-view')),
                         ('Item #2', reverse_lazy('test-view')))),
        ('Other Submenu', (('Other Item #1', reverse_lazy('test-view-2')),
                           ('Ohther Item #2', reverse_lazy('test-view-2'))))
        )
    

class TestView(TestSubmenuMixin, TemplateView):
            template_name='core/test/test_view.html'
