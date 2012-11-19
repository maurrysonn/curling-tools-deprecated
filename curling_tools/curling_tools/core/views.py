# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
# Django Generic Views
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
# Tools
# from curling_tools.core.tools import ChangeListInfosWrapper


class CTAppLabelMixin(object):

    app_label = None

    def get_app_label(self):
        if self.app_label:
            return self.app_label
        return self.__module__.split('.')[-2]



class CTBaseModelMixin(CTAppLabelMixin):
    """
    This mixin define basic infos for Curling Tools views.

    First, this mixin defines infos about model in context,
    such as verbose names, app label.
    Then, this mixin defines a new path to find the file
    templates (in model directory, then app directory and
    finally the template file).
    """

    model = None

    @property
    def model_infos(self):
        "Return a dict with infos about the model."
        # Creation of variable if needed
        if not hasattr(self, '_model_infos'):
            self._model_infos = None
        # Generating data if not yet done
        if self._model_infos is None:
            self._model_infos = {}
            # Specific model data
            if self.model is not None:
                self._model_infos['model'] = self.model
                self._model_infos['app_label'] = \
                    self.model._meta.app_label
                self._model_infos['module_name'] = \
                    self.model._meta.module_name
                self._model_infos['verbose_name'] = \
                    self.model._meta.verbose_name
                self._model_infos['verbose_name_plural'] = \
                    self.model._meta.verbose_name_plural
        return self._model_infos

    def get_template_names(self):
        "Define the search path of templates."
        template_list = []
        module_name = self.model_infos.get('module_name', None)
        app_label = self.model_infos.get('app_label', None)
        base_template_name = u'model%s.html' % self.template_name_suffix        
        # Template parameter of the view
        if self.template_name:
            template_list.append(self.template_name)
        if app_label and module_name:
            # Template of the module
            # e.g. : 'app/module/model_with_suffix.html'
            template_list.append(os.path.join(app_label, module_name,
                                              base_template_name))
            # Template of the app
            # e.g. : 'app/model_with_suffix.html'
            template_list.append(os.path.join(app_label, base_template_name))
        # Default Template
        # e.g. : 'core/model_with_suffix.html'
        template_list.append(os.path.join('core', base_template_name))
        # The list is complete
        return template_list

    def get_context_data(self, **kwargs):
        context = super(CTBaseModelMixin, self).get_context_data(**kwargs)
        # Update context with infos of model
        context[settings.CONTEXT_MODEL_INFOS] = self.model_infos
        return context


class CTSubmenuMixin(object):
    "This mixin define a submenu mechanism."

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


class CTAppHomeMixin(CTAppLabelMixin):
    
    def get_template_names(self):
        template_list = []
        # Template View
        if self.template_name:
            template_list.append(self.template_name)
        # Automatic home template for the app
        app_label = self.get_app_label()
        if app_label:
            template_list.append(os.path.join(
                    app_label, settings.APP_HOME_TEMPLATE))
        # Default home template
        template_list.append(settings.DEFAULT_APP_HOME_TEMPLATE)
        return template_list


class CTModelListMixin(CTBaseModelMixin):
    "Defines mechanism of list object view."
    
    def get_context_data(self, **kwargs):
        context = super(CTModelListMixin, self).get_context_data(**kwargs)
        # TODO : Adding specific data for list
        context[settings.CONTEXT_MODEL_LIST] = {}
        return context


class CTModelDetailMixin(CTBaseModelMixin):
    "Defines mechanism of detail object view."

    def get_context_data(self, **kwargs):
        context = super(CTModelDetailMixin, self).get_context_data(**kwargs)
        # TODO : Adding specific data for detail view
        context[settings.CONTEXT_MODEL_DETAIL] = {}
        return context


class CTModelUpdateMixin(CTBaseModelMixin):
    "Defines mechanism of detail object view."

    def get_cancel_url(self):
        # return self.object.get_absolute_url()
        return None

    def get_context_data(self, **kwargs):
        context = super(CTModelUpdateMixin, self).get_context_data(**kwargs)
        context[settings.CONTEXT_MODEL_EDIT] = {'cancel_url': self.get_cancel_url()}
        return context


class CTModelDeleteMixin(CTBaseModelMixin):
    "Defines mechanism of delete object view."

    def get_cancel_url(self):
        # return self.object.get_absolute_url()
        return None

    def get_success_url(self):
        # Get class params
        if self.success_url:
            return reverse(self.success_url)
        # Else, try to reverse the default url, like 'model-list'
        try:
            list_url = u'%s:%s-list' % (self.model_infos['app_label'],
                                        self.model_infos['module_name'])
            return reverse(list_url)
        except NoReverseMatch:
            # Return Home view...
            return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(CTModelDeleteMixin, self).get_context_data(**kwargs)
        context[settings.CONTEXT_MODEL_DELETE] = {'cancel_url': self.get_cancel_url()}
        return context

# ---------------
# Base Views
# ---------------

class CTTemplateView(CTSubmenuMixin, TemplateView): pass
class CTAppHomeView(CTSubmenuMixin, CTAppHomeMixin, TemplateView): pass
class CTListView(CTSubmenuMixin, CTModelListMixin, ListView): pass
class CTDetailView(CTSubmenuMixin, CTModelDetailMixin, DetailView): pass
class CTCreateView(CTSubmenuMixin, CTBaseModelMixin, CreateView): pass
class CTUpdateView(CTSubmenuMixin, CTModelUpdateMixin, UpdateView): pass
class CTDeleteView(CTSubmenuMixin, CTModelDeleteMixin, DeleteView): pass
