# -*- coding: utf-8 -*-
from curling_tools.base.models import Team
from curling_tools.core.utils import render_json_response, \
    render_json_response_500
from curling_tools.core.views import CTTemplateView, CTSubmenuMixin, \
    CTAppHomeView, CTCreateView, CTListView, CTDetailView, CTUpdateView, \
    CTDeleteView
from curling_tools.tournament_base.models import End
from curling_tools.tournament_schenkel.forms import STGroupForm
from curling_tools.tournament_schenkel.models import SchenkelTournament, \
    SchenkelGroup, SchenkelRound, SchenkelResult, SchenkelMatch
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import View
import django.utils.simplejson as json


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
            messages.error(request, 'Another group already in progress : %s' % current_group)
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


class STGroupFinishMatchesView(View):

    @property
    def group(self):
        if not hasattr(self, '_group'):
            self._group = get_object_or_404(SchenkelGroup,
                                            pk=self.kwargs['pk_group'])
        return self._group

    def get(self, request, *args, **kwargs):
        # Already finished ?
        if self.group.finished:
            return redirect(self.group)
        # If all matches are not finished
        if not self.group.matches_are_finished():
            messages.error(request, _(u'All matches are not finished.'))
            # Go to scoring board
            return redirect(self.group.get_absolute_url_scoring_board())
        # Group can be finished
        self.group.finished = True
        self.group.current = False
        self.group.save()
        # Compute Ranking : TODO
        # MSG if no errors
        messages.success(request, _(u'Group is now finished.'))
        # Go to detail view
        return redirect(self.group)


class STGroupScoringBoardView(STGroupDetailView):
    template_name = u'tournament_schenkel/schenkelgroup/scoring_board.html'
    model = SchenkelGroup
    pk_url_kwarg = 'pk_group'

    def get(self, request, *args, **kwargs):
        response = super(STGroupScoringBoardView, self).get(request, *args, **kwargs)
        # Check if current group or
        # if group is finished
        if self.object.current or self.object.finished:
            return response
        # Msg for user
        messages.error(request, u"This group is not yet started.")
        return redirect(self.object)

    def get_context_data(self, **kwargs):
        context = super(STGroupScoringBoardView, self).get_context_data(**kwargs)
        # Add Ends objects
        context['ends'] = End.objects.all()[:8]
        # JS parameters
        context['url_finish_group'] = reverse('tournament_schenkel:schenkelgroup-finish-matches',
                                            args=[self.tournament.pk, self.round.pk, self.object.pk])
        context['js_opts'] = json.dumps({
                'url_scoring':reverse('tournament_schenkel:match-scoring-end'),
                'url_finish_match': reverse('tournament_schenkel:match-finish'),
                'url_finish_group': context['url_finish_group'],
                })
        return context


class STMatchScoreEndView(View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        # Get match, team, end and score
        try:
            match = SchenkelMatch.objects.get(pk=request.POST['match_pk'])
            team = Team.objects.get(pk=request.POST['team_pk'])
            end = End.objects.get(pk=request.POST['end_pk'])
            score = int(request.POST['score'])
        except(KeyError, ValueError, SchenkelMatch.DoesNotExist, Team.DoesNotExist, End.DoesNotExist):
            return render_json_response_500()
        # Check if match not finished
        if match.finished:
            return render_json_response_500(
                msg=_(u'Match on sheet %s is already finished.' % match.sheet.name))
        # Create the result
        try:
            result = SchenkelResult.objects.create(match=match,
                                                   team=team,
                                                   end=end,
                                                   scoring=score)
        except Exception as e:
            return render_json_response_500(msg=e)
        # Check if match is now finished
        if end.order == 8:
            match.finished = True
            match.save()
            all_matches_finished = match.group.matches_are_finished()
        else:
            all_matches_finished = False
        # Return code response and msg for user
        return render_json_response(
            match_finished=match.finished,
            all_matches_finished=all_matches_finished,
            msg=_(u'<strong>Sheet %s</strong> : <strong>%s</strong> scored <strong>%s</strong> '
                  u'in <strong>end %s</strong>.') % (match.sheet.name, team.name, score, end.order))


class STMatchFinishView(View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            match = SchenkelMatch.objects.get(pk=request.POST['match_pk'])
        except SchenkelMatch.DoesNotExist:
            return render_json_response_500()
        if not match.finished:
            match.finished = True
            match.save()
        return render_json_response(
            match_finished=match.finished,
            all_matches_finished = match.group.matches_are_finished(),
            msg=_(u'<strong>Sheet %s</strong> : Match is finished.' % match.sheet.name))
