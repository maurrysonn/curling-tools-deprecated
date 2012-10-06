# -*- coding: utf-8 -*-
# Django tools
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy
# Core views
from curling_tools.core.views import CTSubmenuMixin, CTListView
# Models module
from curling_tools.base.models import Country


class BaseSubmenu(CTSubmenuMixin):
    "Define a submenu the module."

    submenu_items = (
        (_(u'Countries'),
         ((_(u'List of countries'), reverse_lazy('base:country-list')),
          (_(u'Add a country'), '/base/country/add'))),
        (_(u'Cities'),
         ((_(u'List of cities'), '/base/city/'),
          (_(u'Add a city'), '/base/city/add/'))),
        (_(u'Persons'),
         ((_(u'List of persons'), '/base/person/'),
          (_(u'Add a person'), '/base/person/add/')))
        )
    
class CountryListView(BaseSubmenu, CTListView):
    snippet_model_list = 'base/country_list_snippet.html'
    model = Country
