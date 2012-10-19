# -*- coding: utf-8 -*-
import os

from django.conf import settings
# Django Generic Views
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import BooleanField, NullBooleanField
# Utils
from curling_tools.core.utils import ChangeListInfosWrapper


class CTBaseModelMixin(object):
    """
    This mixin define basic infos for Curling Tools views.

    First, this mixin defines infos about model in context,
    such as verbose names, app label.
    Then, this mixin defines a new path to find the file
    templates (in model directory, then app directory and
    finally the template file).
    """

    @property
    def model_infos(self):
        "Return a dict with infos about the model."
        if not hasattr(self, '_model_infos'):
            self._model_infos = None
        if self._model_infos is None:
            self._model_infos = {}
            self._model_infos['module_name'] = \
                self.model._meta.module_name
            self._model_infos['app_label'] = \
                self.model._meta.app_label
            self._model_infos['verbose_name'] = \
                self.model._meta.verbose_name
            self._model_infos['verbose_name_plural'] = \
                self.model._meta.verbose_name_plural
        return self._model_infos

    def get_template_names(self):
        "Define the search path of templates."
        template_list = []
        module_name = self.model_infos.get('module_name', '')
        app_label = self.model_infos.get('app_label', '')
        base_template_name = u'model%s.html' % self.template_name_suffix
        # Template parameter of the view
        if self.template_name:
            template_list.append(self.template_name)
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
        print "TEMPLATES ="
        print template_list
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





class CTModelListMixin(CTBaseModelMixin):
    "Defines mechanism of list object view."
    snippet_model_list = None

    def get_snippet_model_list(self):
        "Return snippet template for the items list."
        snippet_list = []
        if self.snippet_model_list:
            return self.snippet_model_list
        return settings.DEFAULT_SNIPPET_MODEL_LIST

    def get_context_data(self, **kwargs):
        context = super(CTModelListMixin, self).get_context_data(**kwargs)
        # RENDERING CHANGE LIST INFOS
        model_list_infos = {}
        # Snippet template
        model_list_infos['snippet'] = self.get_snippet_model_list()
        # Update context
        context[settings.CONTEXT_MODEL_LIST] = model_list_infos
        return context


class CTModelDetailMixin(CTBaseModelMixin):
    "Defines mechanism of detail object view."
    snippet_model_detail = None

    def get_snippet_model_detail(self):
        "Return snippet template for the items list."
        snippet_detail = []
        if self.snippet_model_detail:
            return self.snippet_model_detail
        return settings.DEFAULT_SNIPPET_MODEL_DETAIL

    def get_context_data(self, **kwargs):
        context = super(CTModelDetailMixin, self).get_context_data(**kwargs)
        # RENDERING CHANGE LIST INFOS
        model_detail_infos = {}
        # Snippet template
        model_detail_infos['snippet'] = self.get_snippet_model_detail()
        # Update context
        context[settings.CONTEXT_MODEL_DETAIL] = model_detail_infos
        return context

# ---------------
# Base Views
# ---------------

class CTTemplateView(CTSubmenuMixin, TemplateView): pass
class CTListView(CTSubmenuMixin, CTModelListMixin, ListView): pass
class CTDetailView(CTSubmenuMixin, CTModelDetailMixin, DetailView): pass
class CTAppHomeView(CTTemplateView):
    template_name = None




# --
# TODO
class CTModelFormMixin(object):
    pass

class CTModelDeleteMixin(object):
    pass


# ---------------
# TO SAVE ...
# ---------------

# class CTModelListMixin(CTBaseModelMixin):
#     "Defines mechanism of list object view."

#     snippet_model_list = None
#     list_display = ()
#     list_display_links = ()
    
#     @property
#     def cl_wrapper(self):
#         "Accessor of change list infos object."
#         if not hasattr(self, 'cl'):
#             self.cl = ChangeListInfosWrapper(self)
#         return self.cl

#     def get_snippet_model_list(self):
#         "Return snippet template for the items list."
#         snippet_list = []
#         if self.snippet_model_list:
#             return self.snippet_model_list
#         return settings.DEFAULT_SNIPPET_MODEL_LIST

#     def get_queryset(self):
#         "Compute the queryset with GET params."
#         return super(CTModelListMixin, self).get_queryset()

#     def get_context_data(self, **kwargs):
#         context = super(CTModelListMixin, self).get_context_data(**kwargs)
#         # RENDERING CHANGE LIST INFOS
#         model_list_infos = {}
#         # Snippet template
#         model_list_infos['snippet'] = self.get_snippet_model_list()
#         # Change List Infos Wrapper
#         model_list_infos['cl'] = self.cl_wrapper
#         # Update context
#         context[settings.CONTEXT_MODEL_LIST] = model_list_infos
#         return context

# ---------------
# TO DELETE
# ---------------

# class CTModelContextMixin(object):

#     def get_context_data(self, **kwargs):
#         context = super(CTModelContextMixin, self).get_context_data(**kwargs)
#         model_data = {}
#         if self.model:
#             model_data['app_label'] = self.model._meta.app_label
#             model_data['verbose_name'] = self.model._meta.verbose_name
#             model_data['verbose_name_plural'] = self.model._meta.verbose_name_plural
#             # Updating context
#             context['ct_model'] = model_data
#         return context


