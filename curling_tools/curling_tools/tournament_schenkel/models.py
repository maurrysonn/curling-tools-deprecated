# -*- coding: utf-8 -*-
from curling_tools.base.models import Club, Rink, Team
from curling_tools.core.models import CTModel
from curling_tools.tournament_base.models import End, Sheet
from curling_tools.tournament_schenkel.tools import get_results_for_match, \
    add_results_to_ranking, convert_ranking_db_to_team_results, compute_ranking, \
    TeamResult
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _


class STModelMixin(object):

    # ABSOLUTE URL
    def get_absolute_url_name(self):
        return u'%s:tournament-%s%s' % (self.app_label, self.module_name, settings.URL_DETAIL_SUFFIX)

    def get_absolute_url_args(self):
        return [self.tournament.pk, self.pk]

    def get_absolute_url(self):
        return reverse(self.get_absolute_url_name(), args=self.get_absolute_url_args())

    # ABSOLUTE LIST URL
    def get_absolute_url_list_name(self):
        return u'%s:tournament-%s%s' % (self.app_label, self.module_name, settings.URL_LIST_SUFFIX)

    def get_absolute_url_list_args(self):
        return [self.tournament.pk]

    def get_absolute_list_url(self):
        return reverse(self.get_absolute_url_list_name(),
                       args=self.get_absolute_url_list_args())

    # ABSOLUTE EDIT URL
    def get_absolute_url_edit_name(self):
        return u'%s:tournament-%s%s' % (self.app_label, self.module_name, settings.URL_EDIT_SUFFIX)

    def get_absolute_url_edit_args(self):
        return [self.tournament.pk, self.pk]

    def get_absolute_edit_url(self):
        return reverse(self.get_absolute_url_edit_name(),
                       args=self.get_absolute_url_edit_args())

    # ABSOLUTE DELETE URL
    def get_absolute_url_delete_name(self):
        return u'%s:tournament-%s%s' % (self.app_label, self.module_name, settings.URL_DELETE_SUFFIX)

    def get_absolute_url_delete_args(self):
        return [self.tournament.pk, self.pk]

    def get_absolute_delete_url(self):
        return reverse(self.get_absolute_url_delete_name(),
                       args=self.get_absolute_url_delete_args())


class SchenkelTournament(CTModel):
    """
    A basic Tournament Entity

    Define all basics informations and methods of all tournaments.
    """
    name = models.CharField(_(u"name"), max_length=100)
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end_date"))
    club = models.ForeignKey(Club, related_name="tournaments", null=True, blank=True)
    rink = models.ForeignKey(Rink, related_name="tournaments", null=True, blank=True)
    # Tournament Settings
    final_blocked = models.BooleanField(_(u'final is blocked ?'), default=False)
    # last_group_blocked = models.BooleanField(_(u'Last group is blocked ?'))

    def rounds_list(self):
        return self.rounds.order_by('order')

    def is_finished(self):
        # TODO
        return False

    def get_ranking(self):
        """
        Returns global ranking.

        Returns the final ranking of the tournament if is finished,
        else returns None.
        """
        # TODO
        return None

    def get_absolute_dashboard_url(self):
        return reverse('tournament_schenkel:dashboard', args=[self.pk])
    
    def __unicode__(self): return self.name

    class Meta:
        verbose_name = _(u"tournament")
        verbose_name_plural = _(u"tournaments")
        ordering = ["start_date", "name"]


class SchenkelRoundManager(models.Manager):

    def get_prev(self, current_round):
        if current_round.order <= 1:
            return None
        try:
            return super(SchenkelRoundManager, self).get_query_set().get(tournament=current_round.tournament,
                                                                         order=current_round.order-1)
        except SchenkelRound.DoesNotExist:
            return None

    def get_next(self, current_round):
        try:
            return super(SchenkelRoundManager, self).get_query_set().get(tournament=current_round.tournament,
                                                                         order=current_round.order+1)
        except SchenkelRound.DoesNotExist:
            return None


class SchenkelRound(STModelMixin, CTModel):
    """
    A matches round of a tournament.

    Represents a round of a tournament.
    A tournament is generally composed by many Round (4 or 5).
    Each tRound is composed of many Group.
    """
    TYPES_ROUND_CHOICES = (
        ('G', _(u'Group')),
        ('R', _(u'Ranking')),
        ('F', _(u'Final')),
        )
    tournament = models.ForeignKey(SchenkelTournament, related_name='rounds')
    name = models.CharField(_("name"), max_length=100, blank=True)
    # Order degree into the tournament
    order = models.IntegerField(_('order'), default=0)
    # Type of the round
    type = models.CharField(_("type"), max_length=1,
                            choices=TYPES_ROUND_CHOICES, default='G')
    # Manager
    objects = SchenkelRoundManager()

    @property
    def proxy(self):
        # TODO proxies to eliminate 'if' statements
        pass
    
    def groups_list(self):
        return self.groups.order_by('order')

    def finished(self):
        return self.groups.count() > 0 and \
            self.groups.filter(finished=False).count() == 0

    def get_results(self):
        # TODO
        pass

    def compute_ranking_for_group(self, group):
        if not group.finished:
            return []
        if self.type == 'G' or self.type == 'R':
            # Get results for the group
            results = group.get_results()
            # Get old ranking if exists
            # and compute new global results
            if self.order > 1:
                # Type 'Group'
                if self.type == 'G':
                    # Get only results of the group for previous round
                    prev_group = SchenkelGroup.objects.get_prev_round(group)
                    prev_ranking_db = prev_group.get_ranking()
                # Type 'Ranking'
                else:
                    # Get all results of all groups for the previous round
                    prev_round = SchenkelRound.objects.get_prev(self)
                    prev_ranking_db = prev_round.get_ranking()
                # Compute new results
                new_results = add_results_to_ranking(convert_ranking_db_to_team_results(prev_ranking_db), results)
            else:
                new_results = results
            # Compute new ranking
            new_ranking = compute_ranking(new_results)
            # Create GoupRanking objects
            new_ranking_objs = []
            for rank in new_ranking:
                obj = SchenkelGroupRanking.objects.create(group=group, team=rank.team,
                                                          rank=rank.rank, ex_aequo=rank.ex_aequo,
                                                          points=rank.points, ends=rank.ends, stones=rank.stones,
                                                          ends_received=rank.ends_received, stones_received=rank.stones_received)
                new_ranking_objs.append(obj)
            # Try to prepare matches of next round
            next_round_group = SchenkelGroup.objects.get_next_round(group)
            if next_round_group:
                next_round_group.populate_matches()
            return new_ranking_objs
        elif self.type == 'F':
            # If final of tournament not bloked
            # => return same ranking of type 'Ranking'
            # Else:
            #  - Check if only 2 first teams can win the tournament:
            #  - If yes:
            #    - Compute "normal" ranking for other team
            #    - Add the 2 finalist at the begining of the ranking (winner in 1st, looser in 2nd)
            #  - If no:
            #    - Same ranking like type 'Ranking'
            raise NotImplementedError()
            
        else:
            raise NotImplementedError()

    def populate_matches_for_group(self, group):
        if self.order == 1:
            return
        if self.type == 'G':
            prev_round_group = SchenkelGroup.objects.get_prev_round(group)
            ranking_list = prev_round_group.get_ranking()
            if ranking_list:
                i_ranking = iter(ranking_list)
                for match in group.matches_list:
                    match.team_1 = i_ranking.next().team
                    match.team_2 = i_ranking.next().team
                    match.save()
        elif self.type == 'R' or self.type == 'F':
            # Get global ranking of previous round
            prev_round = SchenkelRound.objects.get_prev(self)
            if not prev_round.finished():
                return
            prev_ranking_list = prev_round.get_ranking()
            # Get all matches of this round
            matches_list = SchenkelMatch.objects.filter(group__round=self).order_by('group__order', 'sheet__order')
            i_ranking = iter(prev_ranking_list)
            for match in matches_list:
                match.team_1 = i_ranking.next().team
                match.team_2 = i_ranking.next().team
                match.save()
        else:
            raise NotImplementedError()
            

    def get_ranking_for_group(self, group):
        if not group.finished:
            return []
        ranking = SchenkelGroupRanking.objects.filter(group=group).order_by('rank', 'team')
        if not ranking:
            return self.compute_ranking_for_group(group)
        return ranking

    def get_ranking(self):
        if not self.finished():
            return []
        if self.type == 'G' or self.type == 'R':
            # Get all group rankings
            results_list = []
            for group in self.groups_list():
                results_list.extend(convert_ranking_db_to_team_results(group.get_ranking()))
            # Compute ranks
            ranking_round = compute_ranking(results_list)
        elif self.type == 'F':
            # Check if final is blocked
            # and apply like compute_ranking_for_group() method.
            # TODO
            raise NotImplementedError()
        return ranking_round
        
    def get_name(self):
        if self.name:
            return self.name
        return self.order

    def save(self, *args, **kwargs):
        if not self.pk:
            # Auto-increment the order if creation
            try:
                last_round = self.tournament.rounds.order_by('-order')[0]
                last_order = last_round.order
            except IndexError:
                last_order = 0
            # Updating current level
            self.order = last_order + 1
        return super(SchenkelRound, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s - %s %s (%s - %s)' % (self.tournament,
                                          _(u'Round'),
                                          self.get_name(),
                                          self.order,
                                          self.get_type_display())
    
    class Meta:
        unique_together = ("tournament", "order")
        verbose_name = _(u"round")
        verbose_name_plural = _(u"rounds")
        ordering = ["tournament", "order"]


class SchenkelGroupManager(models.Manager):

    def get_prev_round(self, group):
        prev_round = SchenkelRound.objects.get_prev(group.round)
        if prev_round:
            try:
                return super(SchenkelGroupManager, self).get_query_set().get(round=prev_round, order=group.order)
            except SchenkelGroup.DoesNotExist:
                pass
        return None

    def get_next_round(self, group):
        next_round = SchenkelRound.objects.get_next(group.round)
        if next_round:
            try:
                return super(SchenkelGroupManager, self).get_query_set().get(round=next_round, order=group.order)
            except SchenkelGroup.DoesNotExist:
                pass
        return None
    
    def get_current(self, tournament):
        return super(SchenkelGroupManager, self).get_query_set().get(round__tournament=tournament,
                                                                     current=True)


class SchenkelGroup(STModelMixin, CTModel):
    """
    Represents a group of a round.

    A Group contains all matches of a specific round.
    """
    round = models.ForeignKey(SchenkelRound, related_name='groups')
    name = models.CharField(_(u"name"), max_length=100)
    nb_teams = models.IntegerField(_(u'number of teams'), default=12)
    order = models.IntegerField(_(u'order'), default=1,
                                help_text=_(u"Order of this group in the round."))
    # teams = models.ManyToManyField(Team, related_name="groups", blank=True)
    # Date/Time infos
    date = models.DateField(_('date'))
    time_start = models.TimeField(_(u'start time'))
    time_end = models.TimeField(_(u'end time'))
    # State infos
    current = models.BooleanField(_(u'is current round ?'), default=False)
    finished = models.BooleanField(_(u'is finished ?'), default=False)
    # Manager
    objects = SchenkelGroupManager()

    # @property
    # def nb_current_teams(self):
    #     return self.teams.count()

    def __unicode__(self):
        return u'%s - %s (Order:%s)' % (self.round, self.name, self.order)

    def clean(self):
        if self.nb_teams == 0:
            raise ValidationError(_(u"The number of teams can't be null."))
        if self.nb_teams % 2:
            raise ValidationError(_(u"The number of teams must be even."))

    def save(self, *args, **kwargs):
        if not self.pk:
            # Auto-increment the order if creation
            try:
                last_group = self.round.groups.order_by('-order')[0]
                last_order = last_group.order
            except IndexError:
                last_order = 0
            # Updating current level
            self.order = last_order + 1
        obj = super(SchenkelGroup, self).save(*args, **kwargs)
        # Create match entities
        self._prepare_matches()
        # Return obj
        return obj

    def _prepare_matches(self):
        """
        Creates all matches entities needed.
        
        If already done, do nothing.
        """
        nb_matches_total = self.nb_teams/2
        nb_matches = self.matches.count()
        if nb_matches < nb_matches_total:
            sheet = Sheet.objects.get_first()
            for i in xrange(nb_matches_total):
                SchenkelMatch.objects.get_or_create(group=self, sheet=sheet)
                sheet = Sheet.objects.get_next(current_sheet=sheet)

    def populate_matches(self, ranking_list=None):
        if not self.is_ready:
            self.round.populate_matches_for_group(self)
    
    @property
    def tournament(self):
        return self.round.tournament

    def get_absolute_url_args(self):
        return [self.tournament.pk, self.round.pk, self.pk]

    def get_absolute_url_list_args(self):
        return [self.tournament.pk, self.round.pk]

    def get_absolute_url_edit_args(self):
        return [self.tournament.pk, self.round.pk, self.pk]

    def get_absolute_url_delete_args(self):
        return [self.tournament.pk, self.round.pk, self.pk]

    def get_absolute_url_scoring_board(self):
        return reverse('tournament_schenkel:schenkelgroup-scoring-board',
                       args=[self.round.tournament.pk, self.round.pk, self.pk])

    @property
    def matches_list(self):
        return self.matches.order_by('sheet')
    
    @property
    def teams_list(self):
        teams_list = []
        for m in self.matches_list:
            teams_list.append(m.team_1)
            teams_list.append(m.team_2)
        return teams_list
    
    @property
    def is_ready(self):
        # Group is ready if all its matches are ready.
        matches = self.matches.all()
        if not matches:
            return False
        for match in self.matches_list:
            if not match.is_ready:
                return False
        return True

    def matches_are_finished(self):
        if not self.finished:
            return self.matches.filter(finished=False).count() == 0
        return self.finished

    def get_match_results(self):
        if self.finished:
            return [match.get_complete_results() for match in self.matches_list]
        return []

    def get_results(self):
        results_list = []
        for mr in self.get_match_results():
            results_list.append(mr['team_1'])
            results_list.append(mr['team_2'])
        return results_list
    
    def get_ranking(self):
        if self.finished:
            return self.round.get_ranking_for_group(self)
        return []

    def check_if_final_blocked(self):
        print "CHECK IF FINAL BLOCKED :", self
        # Get ranking of previous round
        prev_round = SchenkelRound.objects.get_prev(self.round)
        prev_ranking = prev_round.get_ranking()
        # print "PREV RANKING"
        # for rank in prev_ranking: print "\t", rank
        # Filter teams in group
        teams_list = self.teams_list
        prev_ranking = [rank for rank in prev_ranking if rank.team in teams_list]
        # print "PREV RANKING FILTERD"
        # for rank in prev_ranking: print "\t", rank
        # Compute the potential new ranking
        # (worst result for team #1, team #2 and best for team #3)
        new_results = [TeamResult(team=prev_ranking[0].team, points=1),
                       TeamResult(team=prev_ranking[1].team, points=1),
                       TeamResult(team=prev_ranking[2].team, points=2, ends=8, stones=64)]
        new_ranking = compute_ranking(add_results_to_ranking(prev_ranking[:3], new_results))
        print "NEW POTENTIAL RANKING"
        for rank in new_ranking: print "\t", rank
        # If team #3 win, final can't be blocked
        if new_ranking[0].team == prev_ranking[2].team:
            return False
        return True


    class Meta:
        verbose_name = _(u'group')
        verbose_name_plural = _(u'groups')
        ordering = ['round', 'order']
        unique_together = ('round', 'order')


class SchenkelGroupRanking(models.Model):
    """
    Model which regroups informations about ranking of round for a specific group.

    Ranking informations for each team of a group are saved:
    rank, points, ends, stones, ends recevived and stones received.
    """
    group = models.ForeignKey(SchenkelGroup)
    team = models.ForeignKey(Team)
    
    rank = models.PositiveIntegerField(_(u"rank"))
    ex_aequo = models.BooleanField(_(u"ex aequo"), default=False)
    points = models.PositiveIntegerField(_(u"points"))
    ends = models.PositiveIntegerField(_(u"ends"))
    stones = models.PositiveIntegerField(_(u"stones"))
    ends_received = models.PositiveIntegerField(_(u"ends received"))
    stones_received = models.PositiveIntegerField(_(u"stones received"))

    def __unicode__(self):
        return _(u"Rank : %s - %s : %s (P:%s E:%s S:%s ER:%s SR:%s)") \
            % (self.group, self.team, self.rank, self.points, self.ends, self.stones,
               self.ends_received, self.stones_received)
    
    class Meta:
        verbose_name = _(u"Ranking")
        verbose_name_plural = _(u"Rankings")        
        ordering = ('group', 'rank')
        unique_together = ('group', 'team')
        
class SchenkelMatch(models.Model):
    """
    A Match Entity
    """
    group = models.ForeignKey(SchenkelGroup, related_name='matches')
    team_1 = models.ForeignKey(Team, related_name='matches_1',
                               blank=True, null=True)
    team_2 = models.ForeignKey(Team, related_name='matches_2',
                               blank=True, null=True)
    sheet = models.ForeignKey(Sheet, related_name='matches')
    hammer = models.ForeignKey(Team, blank=True, null=True)
    finished = models.BooleanField(_(u'is finished ?'), default=False)

    @property
    def is_ready(self):
        return self.group and self.team_1 and self.team_2 and self.sheet

    def get_absolute_url(self):
        return '/'

    def __unicode__(self):
        return u"%s - %s : %s vs %s" % (self.group, self.sheet, self.team_1, self.team_2)

    @property
    def results_list(self):
        return self.results.all().order_by('end__order')

    @property
    def winner(self):
        scoring_team_1 = self.results.filter(team=self.team_1).aggregate(models.Sum('scoring'))['scoring__sum']
        scoring_team_2 = self.results.filter(team=self.team_2).aggregate(models.Sum('scoring'))['scoring__sum']
        if scoring_team_1 > scoring_team_2:
            return self.team_1
        elif scoring_team_2 > scoring_team_1:
            return self.team_2
        else:
            return None

    def get_complete_results(self):
        if self.finished:
            global_results = get_results_for_match(self)
            return global_results
        return []

    class Meta:
        verbose_name = _(u"match")
        verbose_name_plural = _(u"matches")
        unique_together = ('group', 'sheet')
        ordering = ["group", "sheet"]


class SchenkelResult(models.Model):
    """
    Result of a end's match.

    Represents the score of a team for a particular end of a match.
    """
    match = models.ForeignKey(SchenkelMatch, related_name='results')
    team = models.ForeignKey(Team, related_name='results')
    end = models.ForeignKey(End, related_name='results')
    scoring = models.IntegerField(_(u'scoring'), blank=True, null=True)

    def __unicode__(self):
        return u"%s (%s) : %s - %s" % (self.match, self.end, self.scoring, self.team)

    class Meta:
        unique_together = ('match', 'end')
        verbose_name = _(u"result")
        verbose_name_plural = _(u"results")
        ordering = ["match","team"]
