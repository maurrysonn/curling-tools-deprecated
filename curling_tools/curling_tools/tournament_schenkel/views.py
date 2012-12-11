# -*- coding: utf-8 -*-
# Django tools
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
# Django View
from django.views.generic import View
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
                                                      SchenkelRound)
# Module forms
from curling_tools.tournament_schenkel.forms import STGroupForm, STGroupAutoFilledForm


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

class STGroupMixin(object):

    @property
    def round(self):
        if not hasattr(self, '_round'):
            self._round = get_object_or_404(SchenkelRound,
                                            pk=self.kwargs['pk_round'])
        return self._round

    def get_context_data(self, **kwargs):
        context = super(STGroupMixin, self).get_context_data(**kwargs)
        context['ct_round'] = self.round
        return context
    

class STGroupListView(STGroupMixin, STDashboardSubmenu, STBaseMixin, CTListView):

    model = SchenkelGroup

    def get_queryset(self):
        return super(CTListView, self).get_queryset().filter(round=self.round)


class STGroupCreateView(STGroupMixin, STBaseCreateView):

    model = SchenkelGroup

    def _is_auto_filled_group(self):
        return (self.round.order > 1) and (self.round.type == 'G')

    def get_form_class(self):
        # if self._is_auto_filled_group:
        #     return STGroupAutoFilledForm
        return STGroupForm

    def get_initial(self):
        data = {'round': self.round}
        # if self._is_auto_filled_group:
        #     prev_group = SchenkelGroup.objects.get_prev_round(self.round)
        #     if prev_group:
        #         data['name'] = prev_group.name
        #         data['nb_teams'] = prev_group.nb_teams
        return data

class STGroupUpdateView(STGroupMixin, STBaseUpdateView):
    
    model = SchenkelGroup
    form_class = STGroupForm

class STGroupDetailView(STGroupMixin, STBaseDetailView): pass

class STGroupStartMatchesView(STGroupMixin, STBaseMixin, View):

    http_method_names = ['get']

    @property
    def group(self):
        if not hasattr(self, '_group'):
            self._group = get_object_or_404(SchenkelGroup,
                                            pk=self.kwargs['pk_group'])
        return self._group

    def get(self, request, *args, **kwargs):
        # Check if already current
        if self.group.current:
            return redirect(self.group.get_absolute_url_scoring_board())
        # Check if another Group in progress
        try:
            current_group = SchenkelGroup.objects.get_current(self.tournament)
            # Msg for user
            messages.error(request, 'Another group already in progress.')
            # Redirect to detail group view
            return redirect(self.group)
        except SchenkelGroup.DoesNotExist:
            # No group in progress, we continue
            pass
        # Check if Group is ready to start
        if not self.group.is_ready:
            # Msg for user
            messages.error(request, u"Group doesn't ready to start.")
            return redirect(self.group)
        # It's OK, so we enable the group
        self.group.current = True
        self.group.save()
        # Redirect to Scoring Board
        return redirect(self.group.get_absolute_url_scoring_board())


class STGroupScoringBoardView(STGroupMixin, STDashboardSubmenu, STBaseMixin, CTTemplateView):
    template_name = u'tournament_schenkel/schenkelgroup/scoring_board.html'
