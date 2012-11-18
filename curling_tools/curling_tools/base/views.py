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
from curling_tools.base.models import (Country, Person, Address,
                                       Player, Coach, Club, Rink)
# Forms module
from curling_tools.base.forms import (PersonPlayerForm, PersonCoachForm,
                                      ClubForm, RinkForm)


class BaseSubmenu(CTSubmenuMixin):
    "Define a submenu the module."

    submenu_items = (
        (_(u'Countries'),
         ((_(u'List of countries'), reverse_lazy('base:country-list')),
          (_(u'Add a country'), reverse_lazy('base:country-add')))),
        (_(u'Cities'),
         ((_(u'List of cities'), reverse_lazy('base:city-list')),
          (_(u'Add a city'), reverse_lazy('base:city-add')))),
        (_(u'Persons'),
         ((_(u'List of persons'), reverse_lazy('base:person-list')),
          (_(u'Add a person'), reverse_lazy('base:person-add')))),
        (_(u'Clubs'),
         ((_(u'List of clubs'), reverse_lazy('base:club-list')),
          (_(u'Add a club'), reverse_lazy('base:club-add')))),
        (_(u'Rinks'),
         ((_(u'List of rinks'), reverse_lazy('base:rink-list')),
          (_(u'Add a rink'), reverse_lazy('base:rink-add')))),
        (_(u'Teams'),
         ((_(u'List of teams'), reverse_lazy('base:team-list')),
          (_(u'Add a team'), reverse_lazy('base:team-add')))),
        )
    

class BaseHomeView(BaseSubmenu, CTAppHomeView): pass


# ----------------------------
# Objects Related Mixins
# ----------------------------

class ObjectRelatedMixin(object):
    rel_model = None

    @property
    def rel_obj(self):
        rel_attr = '_%s' % (self.rel_model._meta.module_name)
        if not hasattr(self, rel_attr):
            setattr(self, rel_attr, get_object_or_404(
                    self.rel_model, pk=self.kwargs.get('pk', 0)))
        return getattr(self, rel_attr)
    
    def get_success_url(self):
        return self.rel_obj.get_absolute_url()


# ----------------------------
# Person Mixins
# ----------------------------

class PersonRelatedMixin(ObjectRelatedMixin):
    rel_model = Person


class PersonRelatedCreateMixin(PersonRelatedMixin, BaseSubmenu, CTCreateView):
    """
    View that create a player from a person detail view.
    """
    def form_valid(self, form):
        # Create instance object
        self.object = form.save(commit=False)
        # Update person attr
        self.object.person = self.rel_obj
        # Save the new object
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# ----------------------------
# Address Related Mixin
# ----------------------------

class AddressRelatedUpdateMixin(ObjectRelatedMixin, BaseSubmenu, CTUpdateView):
    model = Address

    def get_object(self, *args, **kwargs):
        return self.rel_obj.address

    def form_valid(self, form):
        if self.object is None:
            address = form.save()
            self.rel_obj.address = address
            self.rel_obj.save()
        return super(AddressRelatedUpdateMixin, self).form_valid(form)

# ----------------------------
# Person Views
# ----------------------------


class PersonAddressUpdateView(PersonRelatedMixin, AddressRelatedUpdateMixin,
                              BaseSubmenu, CTUpdateView): pass


class PersonPlayerCreateView(PersonRelatedCreateMixin):
    model = Player
    form_class = PersonPlayerForm


class PersonPlayerUpdateView(PersonRelatedMixin, BaseSubmenu, CTUpdateView):
    """
    View that edit a player infos from a person detail view.
    """
    model = Player
    form_class = PersonPlayerForm

    def get_object(self, *args, **kwargs):
        return self.rel_obj.player


class PersonCoachCreateView(PersonRelatedCreateMixin):
    model = Coach
    form_class = PersonCoachForm


class PersonCoachUpdateView(PersonRelatedMixin, BaseSubmenu, CTUpdateView):
    """
    View that edit a player infos from a person detail view.
    """
    model = Coach
    form_class = PersonCoachForm

    def get_object(self, *args, **kwargs):
        return self.rel_obj.coach


# ------------
# Club Views
# ------------

class ClubRelatedMixin(ObjectRelatedMixin):
    rel_model = Club

class ClubAddressUpdateView(ClubRelatedMixin, AddressRelatedUpdateMixin,
                              BaseSubmenu, CTUpdateView): pass


# ------------
# Rink Views
# ------------

class RinkRelatedMixin(ObjectRelatedMixin):
    rel_model = Rink

class RinkAddressUpdateView(RinkRelatedMixin, AddressRelatedUpdateMixin,
                              BaseSubmenu, CTUpdateView): pass


# ------------
# Player Views
# ------------

# def player_update_view(request, pk):
#     player = get_object_or_404(Player, pk=pk)
#     if request.method == 'POST':
#         player_form = PlayerForm(request.POST, instance=player, prefix="player")
#         person_form = PersonForm(request.POST, instance=player.person, prefix="person")
#         if person_form.is_valid() and player_form.is_valid():
#             person = person_form.save()
#             player = player_form.save()
#             return HttpResponseRedirect(player.get_absolute_url())
#     else:
#         person_form = PersonForm(instance=person, prefix='person')
#         player_form = PlayerForm(instance=person.player, prefix="player")
#     return render_to_response(get_template_names_for_model(Player),
#                               {'player_form': player_form,
#                                'person_form': person_form,},
#                               context_instance=RequestContext(request))
