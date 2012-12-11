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

    def groups_list(self):
        return self.groups.order_by('order')

    def is_finished(self):
        nb_groups_list = self.groups.all().count()        
        if nb_groups_list > 0:
            return self.groups.filter(finished=True).count() == nb_groups_list
        return False

    def get_results(self):
        # TODO
        pass

    def get_ranking(self):
        # TODO
        pass

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
                                          self.get_type_display(),
                                          self.order)
    
    class Meta:
        unique_together = ("tournament", "order")
        verbose_name = _(u"round")
        verbose_name_plural = _(u"rounds")
        ordering = ["tournament", "order"]






class SchenkelGroup(STModelMixin, CTModel):
    """
    Represents a group of a round.

    A Group contains all matches of a specific round.
    """
    round = models.ForeignKey(SchenkelRound, related_name='rounds')
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
        obj = super(SchenkelRound, self).save(*args, **kwargs)
        # Create match entities
        self._prepare_matches()
        # Return obj
        return obj

    def _prepare_matches(self):
        """
        Creates all matches entities needed.
        
        If already done, do nothing.
        """
        print "PREPARE MATCHES"
        nb_matches_total = self.nb_teams/2
        print "nb_matches_total :", nb_matches_total
        sheet = Sheet.objects.get_first()
        nb_matches = self.matches.count()
        print "nb_matches :", nb_matches
        if nb_matches < nb_matches_total:
            for i in xrange(nb_matches_total):
                print "Create match : sheet =", sheet
                SchenkelMatch.objects.get_or_create(group=self, sheet=sheet)
                sheet = Sheet.objects.get_next(current_sheet=sheet)

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

    @property
    def matches_list(self):
        return self.matches.order_by('sheet')
    
    # @property
    # def teams_list(self):
    #     return None

    # def matches_is_created(self):
    #     pass

    # def matches_is_ready(self):
    #     return False

    # def populate_matches(self):
    #     pass

    # def get_results(self):
    #     return None

    # def get_ranking(self):
    #     return None

    class Meta:
        verbose_name = _(u'group')
        verbose_name_plural = _(u'groups')
        ordering = ['round', 'order']
        unique_together = ('round', 'order')


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

    def is_ready(self):
        return self.group and self.team_1 and self.team_2 and self.sheet

    def get_absolute_url(self):
        return '/'

    def __unicode__(self):
        return u"%s (%s) : %s - %s" % (self.group, self.sheet, self.team_1, self.team_2)

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
