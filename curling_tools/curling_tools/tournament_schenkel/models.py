# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
# CT core
from curling_tools.core.models import CTModel
# CT base
from curling_tools.base.models import Club, Rink, Team
# CT tournament base
from curling_tools.tournament_base.models import End, Sheet


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


    def main_rounds_list(self):
        return self.tournament_rounds.order_by('level')

    def groups_list(self):
        return self.groups.order_by('level', 'order')

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


class SchenkelTournamentRound(STModelMixin, CTModel):
    """
    A matches round of a tournament.

    Represents a global round of a tournament.
    A tournament is genrally composed by many TournamentRound (4 or 5).
    Each TournamentRound is composed of many Round (1 round for each Group).
    """
    TYPES_ROUND_CHOICES = (
        ('G', _(u'Group')),
        ('R', _(u'Ranking')),
        ('F', _(u'Final')),
        )
    tournament = models.ForeignKey(SchenkelTournament, related_name='tournament_rounds')
    name = models.CharField(_("name"), max_length=100, blank=True)
    # Level degree into the tournament
    level = models.IntegerField(_('level'), default=1)
    # Type of the round
    type = models.CharField(_("type"), max_length=1,
                            choices=TYPES_ROUND_CHOICES, default='G')

    def rounds_list(self):
        return self.rounds.order_by('group__order')

    def is_finished(self):
        nb_rounds_list = self.rounds.all().count()        
        if nb_rounds_list:
            return self.rounds.filter(finished=True).count() == nb_rounds_list
        return False

    def get_results(self):
        # TODO
        pass

    def get_ranking(self):
        # TODO
        pass

    def save(self, *args, **kwargs):
        # If creation
        if not self.pk:
            # Auto-increment the level
            try:
                last_round = self.tournament.tournament_rounds\
                    .filter(tournament=self.tournament).order_by('-level')[0]
                last_level = last_round.level
                last_type = last_round.type
            except IndexError:
                last_level = 0
            # Updating current level
            self.level = last_level + 1
        return super(SchenkelTournamentRound, self).save(*args, **kwargs)

    def __unicode__(self):
        txt = u""
        if self.name:
            txt = u"%s " % self.name
        txt += u"(%s - %s)" % (self.get_type_display(), self.level)
        return u'%s - %s %s' % (self.tournament, _(u'Main Round'), txt)
    
    class Meta:
        unique_together = ("tournament", "level")
        verbose_name = _(u"main round")
        verbose_name_plural = _(u"main rounds")
        ordering = ["tournament", "level"]


class SchenkelGroup(STModelMixin, CTModel):
    """
    Represents a group of a round.
    """
    tournament = models.ForeignKey(SchenkelTournament, related_name='groups')
    name = models.CharField(_(u"name"), max_length=100)
    teams = models.ManyToManyField(Team, related_name="groups", blank=True)
    nb_teams = models.IntegerField(_(u'number of teams'), default=12)
    
    level = models.IntegerField(_(u'level'), default=1,
                                help_text=_(u"Level of this group in the tournament. "
                                            u"(The level is increased for each global ranking.)"))
    order = models.IntegerField(_(u'order'), default=1,
                                help_text=_(u"Order of this group in the tournament round."))

    @property
    def nb_current_teams(self):
        return self.teams.count()

    def __unicode__(self):
        return u'%s - %s (Level:%s - Order:%s)' % (self.tournament, self.name, self.level, self.order)

    def clean(self):
        if self.nb_teams == 0:
            raise ValidationError(_(u"The number of teams can't be null."))
        if self.nb_teams % 2:
            raise ValidationError(_(u"The number of teams must be even."))

    class Meta:
        verbose_name = _(u'group')
        verbose_name_plural = _(u'groups')
        ordering = ['tournament', 'level', 'order']
        unique_together = ('tournament', 'level', 'order')


class SchenkelRound(STModelMixin, CTModel):
    """
    A Round Entity

    A round regroups all matches of a specific group.
    """
    tournament_round = models.ForeignKey(SchenkelTournamentRound, related_name='rounds')
    group = models.ForeignKey(SchenkelGroup, related_name='rounds')
    # Date/Time infos
    date = models.DateField(_('date'))
    time_start = models.TimeField(_(u'start time'))
    time_end = models.TimeField(_(u'end time'))
    # State infos
    current = models.BooleanField(_(u'is current round ?'), default=False)
    finished = models.BooleanField(_(u'is finished ?'), default=False)

    def _prepare_matches(self):
        """
        Creates all matches entities needed.
        
        If already done, do nothing.
        """
        print "PREPARE MATCHES"
        nb_matches_total = self.group.nb_teams/2
        print "nb_matches_total :", nb_matches_total
        sheet = Sheet.objects.get_first()
        nb_matches = self.matches.count()
        print "nb_matches :", nb_matches
        if nb_matches < nb_matches_total:
            for i in xrange(nb_matches_total):
                print "Create match : sheet =", sheet
                SchenkelMatch.objects.get_or_create(round=self, sheet=sheet)
                sheet = Sheet.objects.get_next(current_sheet=sheet)

    def save(self, *args, **kwargs):
        obj = super(SchenkelRound, self).save(*args, **kwargs)
        # Create match entities
        self._prepare_matches()
        # Return obj
        return obj

    @property
    def tournament(self):
        return self.tournament_round.tournament

    def get_absolute_url_args(self):
        return [self.tournament.pk, self.tournament_round.pk, self.pk]

    def get_absolute_url_list_args(self):
        return [self.tournament.pk, self.tournament_round.pk]

    def get_absolute_url_edit_args(self):
        return [self.tournament.pk, self.tournament_round.pk, self.pk]

    def get_absolute_url_delete_args(self):
        return [self.tournament.pk, self.tournament_round.pk, self.pk]

    def get_matches(self):
        return self.matches.order_by('sheet')
    
    def get_teams(self):
        return None

    def matches_is_created(self):
        pass

    def matches_is_ready(self):
        return False

    def prepare_matches(self):
        pass

    def populate_matches(self):
        pass

    def get_results(self):
        return None

    def get_ranking(self):
        return None

    def __unicode__(self):
        return u"%s - %s" % (self.tournament_round, self.group)

    class Meta:
        verbose_name = _(u"round")
        verbose_name_plural = _(u"rounds")
        ordering = ["tournament_round", "group"]


class SchenkelMatch(models.Model):
    """
    A Match Entity
    """
    round = models.ForeignKey(SchenkelRound, related_name='matches')
    team_1 = models.ForeignKey(Team, related_name='matches_1',
                               blank=True, null=True)
    team_2 = models.ForeignKey(Team, related_name='matches_2',
                               blank=True, null=True)
    sheet = models.ForeignKey(Sheet, related_name='matches')
    hammer = models.ForeignKey(Team, blank=True, null=True)
    finished = models.BooleanField(_(u'is finished ?'), default=False)

    def is_ready(self):
        return self.round and self.team_1 and self.team_2 and self.sheet

    def get_absolute_url(self):
        return '/'

    def __unicode__(self):
        return u"%s (%s) : %s - %s" % (self.round, self.sheet, self.team_1, self.team_2)

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

    class Meta:
        verbose_name = _(u"match")
        verbose_name_plural = _(u"matches")
        unique_together = ('round', 'sheet')
        ordering = ["round", "sheet"]


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
