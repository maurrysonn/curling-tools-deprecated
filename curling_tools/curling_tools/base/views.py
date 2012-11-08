# -*- coding: utf-8 -*-
# Django tools
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
# Core views
from curling_tools.core.views import (CTSubmenuMixin,
                                      CTAppHomeView,
                                      CTUpdateView)
# Models module
from curling_tools.base.models import Country, Person, Address


class BaseSubmenu(CTSubmenuMixin):
    "Define a submenu the module."

    submenu_items = (
        (_(u'Countries'),
         ((_(u'List of countries'), '/base/country/'),
          (_(u'Add a country'), '/base/country/add'))),
        (_(u'Cities'),
         ((_(u'List of cities'), '/base/city/'),
          (_(u'Add a city'), '/base/city/add/'))),
        (_(u'Persons'),
         ((_(u'List of persons'), '/base/person/'),
          (_(u'Add a person'), '/base/person/add/')))
        )
    

class BaseHomeView(BaseSubmenu, CTAppHomeView): pass


class PersonAddressUpdateView(BaseSubmenu, CTUpdateView):

    model = Address

    def get_queryset(self):
        return Person.objects.all()

    def get_object(self, *args, **kwargs):
        # Get the person object
        person = super(PersonAddressUpdateView, self).get_object()
        # Return the address
        return person.address

    def get_success_url(self):
        return reverse('base:person-detail', args=[self.get_object().person.pk])
