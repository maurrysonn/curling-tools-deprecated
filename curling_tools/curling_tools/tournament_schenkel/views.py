# -*- coding: utf-8 -*-
# Django tools
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
# CT views
from curling_tools.core.views import (CTTemplateView,
                                      CTSubmenuMixin,
                                      CTAppHomeView,
                                      CTCreateView,
                                      CTListView,
                                      CTDetailView,
                                      CTUpdateView,
                                      CTDeleteView)
# Module models
from curling_tools.tournament_schenkel.models import (SchenkelTournament,
                                                      SchenkelGroup,
                                                      SchenkelTournamentRound,
                                                      SchenkelRound)
# Module forms
from curling_tools.tournament_schenkel.forms import STRoundForm


# -------------------------------------
# BASE MIXINS
# -------------------------------------

class STSubmenu(CTSubmenuMixin):
    "Define a submenu for the module."

    submenu_items = (
        (_(u'Tournaments'),
         ((_(u'List of tournaments'), reverse_lazy('tournament_schenkel:schenkeltournament-list')),
          (_(u'Add a tournament'), reverse_lazy('tournament_schenkel:schenkeltournament-add')))),
        )


class STDashboardSubmenu(CTSubmenuMixin):

    def get_submenu_items(self):
        submenu_items = (
            (u'%s' % self.tournament.name,
             ((_(u'Dashboard'), reverse('tournament_schenkel:dashboard', args=[self.tournament.pk])),
              )),
            )
        return submenu_items


class STBaseMixin(object):

    @property
    def tournament(self):
        if not hasattr(self, '_tournament'):
            self._tournament = get_object_or_404(SchenkelTournament,
                                                 pk=self.kwargs['pk_tournament'])
        return self._tournament

    def get_context_data(self, **kwargs):
        context = super(STBaseMixin, self).get_context_data(**kwargs)
        context['ct_tournament'] = self.tournament
        return context


# -------------------------------------
# BASE VIEWS
# -------------------------------------

class STBaseCreateView(STDashboardSubmenu, STBaseMixin, CTCreateView):
    def get_initial(self):
        return {'tournament': self.tournament}

class STBaseUpdateView(STDashboardSubmenu, STBaseMixin, CTUpdateView): pass

class STBaseDeleteView(STDashboardSubmenu, STBaseMixin, CTDeleteView):
    def get_success_url(self):
        return self.object.get_absolute_list_url()

class STBaseDetailView(STDashboardSubmenu, STBaseMixin, CTDetailView): pass

class STBaseListView(STDashboardSubmenu, STBaseMixin, CTListView):
    def get_queryset(self):
        return super(STBaseListView, self).get_queryset().filter(tournament=self.tournament)



# -------------------------------------
# VIEWS
# -------------------------------------

class STHomeView(STSubmenu, CTAppHomeView): pass


class STDashboardView(STDashboardSubmenu, STBaseMixin, CTTemplateView):
    
    template_name = 'tournament_schenkel/schenkeltournament/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super(STDashboardView, self).get_context_data(**kwargs)
        return context


# -------------------------------------
# GROUP VIEWS
# -------------------------------------

class STGroupListView(STBaseListView):

    model = SchenkelGroup

    def get_queryset(self):
        self.tournament.groups.order_by('level', 'order')

# -------------------------------------
# ROUND VIEWS
# -------------------------------------

class STRoundMixin(object):

    @property
    def tournament_round(self):
        if not hasattr(self, '_tournament_round'):
            self._tournament_round = get_object_or_404(SchenkelTournamentRound,
                                                       pk=self.kwargs['pk_tournament_round'])
        return self._tournament_round

    def get_context_data(self, **kwargs):
        context = super(STRoundMixin, self).get_context_data(**kwargs)
        context['ct_tournament_round'] = self.tournament_round
        return context
    

class STRoundListView(STRoundMixin, STDashboardSubmenu, STBaseMixin, CTListView):

    model = SchenkelRound

    def get_queryset(self):
        return super(CTListView, self).get_queryset().filter(tournament_round=self.tournament_round)


class STRoundCreateView(STRoundMixin, STBaseCreateView):

    model = SchenkelRound
    form_class = STRoundForm

    def get_initial(self):
        return {'tournament_round': self.tournament_round}

class STRoundUpdateView(STRoundMixin, STBaseUpdateView):
    
    model = SchenkelRound
    form_class = STRoundForm

class STRoundDetailView(STRoundMixin, STBaseDetailView): pass

