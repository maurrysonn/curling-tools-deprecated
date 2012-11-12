# -*- coding: utf-8 -*-
# Django tools
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Core views
from curling_tools.core.views import (CTSubmenuMixin,
                                      CTAppHomeView,
                                      CTUpdateView,
                                      CTCreateView)
# Models module
from curling_tools.base.models import Country, Person, Address, Player
# Forms module
from curling_tools.base.forms import PersonPlayerForm


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


# ------------
# Person views
# ------------

class PersonAttrMixin(object):

    @property
    def person(self):
        if not hasattr(self, '_person'):
            self._person = get_object_or_404(
                Person, pk=self.kwargs.get('pk', 0))
        return self._person
    

class PersonAddressUpdateView(PersonAttrMixin, BaseSubmenu, CTUpdateView):

    model = Address

    def get_object(self, *args, **kwargs):
        # Return the address
        return self.person.address

    def get_success_url(self):
        return reverse('base:person-detail', args=[self.person.pk])

    def form_valid(self, form):
        if self.object is None:
            address = form.save()
            self.person.address = address
            self.person.save()
        return super(PersonAddressUpdateView, self).form_valid(form)


# ------------
# Player views
# ------------

class PersonPlayerCreateView(PersonAttrMixin, BaseSubmenu, CTCreateView):
    """
    View that create a player from a person detail view.
    """
    model = Player
    form_class = PersonPlayerForm
    
    def get_success_url(self):
        return self.person.get_absolute_url()

    def form_valid(self, form):
        # Create instance object
        self.object = form.save(commit=False)
        # Update person attr
        self.object.person = self.person
        # Save the new object
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PersonPlayerUpdateView(PersonAttrMixin, BaseSubmenu, CTUpdateView):
    """
    View that edit a player infos from a person detail view.
    """
    model = Player
    form_class = PersonPlayerForm

    def get_object(self, *args, **kwargs):
        return self.person.player
        # # Get the person object
        # person = super(PersonPlayerUpdateView, self).get_object()
        # # Return the address
        # return person.player
    
    def get_success_url(self):
        return reverse('base:person-detail', args=[self.get_object().person.pk])
