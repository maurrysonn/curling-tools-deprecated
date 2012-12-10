# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from curling_tools.core.models import CTModel


# -------------------------------
# Statics Ressources of countries
# -------------------------------
STATIC_FLAGS_COUNTRIES = 'base/images/flags'
FLAGS_COUNTRIES_EXT = '.png'
DEFAULT_FLAG_COUNTRIES = 'default'


# --------------------
# Geo Items Models
# --------------------
class Country(CTModel):
    """
    A basic country entity
    """
    name = models.CharField(_('name'), max_length=50, unique=True)
    short_name = models.CharField(_(u'short name'), max_length=5, blank=True)
    code = models.CharField(_('code'), max_length=5, unique=True)
    flag = models.CharField(_('flag'), max_length=100, blank=True)

    @property
    def flag_path(self):
        if self.flag:
            file_path = u'%s%s' % (self.flag, FLAGS_COUNTRIES_EXT)
        else:
            file_path = u'%s%s' % (DEFAULT_FLAG_COUNTRIES, FLAGS_COUNTRIES_EXT)
        path = os.path.join(STATIC_FLAGS_COUNTRIES, file_path)
        return path

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.code)

    class Meta:
        verbose_name = _(u'country')
        verbose_name_plural = _(u'countries')
        ordering = ('name',)


class City(CTModel):
    """
    A basic city entity
    """

    name = models.CharField(_(u'name'), max_length=50)
    short_name = models.CharField(_(u'short name'), max_length=5, blank=True)
    default_zipcode = models.CharField(_(u'zipcode'), max_length=10, blank=True)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country.name)

    class Meta:
        verbose_name = _(u'city')
        verbose_name_plural = _(u'cities')
        ordering = ('name',)


class Address(models.Model):
    """
    A basic address informations
    """

    number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=100, blank=True)
    extra = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.ForeignKey(City)
    # Extra city informations, like CEDEX
    extra_city = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u'%s' % (self.city)

    class Meta:
        verbose_name = _(u'address')
        verbose_name_plural = _(u'addresses')


# --------------------
# Club Model
# --------------------

class Club(CTModel):
    """
    A Club Entity
    """
    name = models.CharField(_(u'name'), max_length=100)
    short_name = models.CharField(_(u'short name'), max_length=10, blank=True)
    address = models.OneToOneField(Address, blank=True, null=True)

    def __unicode__(self):
        short_name_txt = u""
        if self.short_name:
            short_name_txt = u" (%s)" % self.short_name
        return u"%s%s" % (self.name, short_name_txt)

    class Meta:
        verbose_name = _(u'club')
        verbose_name_plural = _(u'clubs')
        ordering = ('name',)



# --------------------
# Place Model
# --------------------

class Rink(CTModel):
    """
    A Rink Entity
    """
    name = models.CharField(_(u"name"), max_length=100)
    address = models.OneToOneField(Address, blank=True, null=True)

    def __unicode__(self):
        city_str = u''
        if self.address:
            city_str = u' (%s - %s)' % (self.address.city.name, self.address.city.country.name)
        return u'%s%s' % (self.name, city_str)

    class Meta:
        verbose_name = _(u'rink')
        verbose_name_plural = _(u'rinks')
        ordering = ('name',)


# --------------------
# Persons Models
# --------------------

class Person(CTModel):
    """
    A basic person entity
    """
    first_name = models.CharField(_(u'first name'), max_length=50)
    last_name = models.CharField(_(u'last name'), max_length=50)
    nickname = models.CharField(_(u'nickname'), max_length=50, blank=True)
    phone = models.CharField(_(u'phone'), max_length=20, blank=True)
    mobile_phone = models.CharField(_(u'mobile phone'), max_length=20, blank=True)
    email = models.EmailField(_(u'email'), blank=True)
    dob = models.DateField(_(u'date of birth'), blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True)
    photo = models.ImageField(_(u'photo'), upload_to='base/person', max_length=200, blank=True)

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.full_name

    class Meta:
        verbose_name = _(u'person')
        verbose_name_plural = _(u'persons')
        ordering = ('last_name', 'first_name')


class Player(CTModel):
    """
    A Player Entity
    """
    person = models.OneToOneField(Person, unique=True)
    licence_number = models.CharField(_(u'licence number'), max_length=50, blank=True, null=True)
    club = models.ForeignKey(Club, related_name='players')
    player_since = models.DateField(_(u'Player since'), blank=True, null=True)

    def __unicode__(self):
        return self.person.__unicode__()

    class Meta:
        verbose_name = _(u'player')
        verbose_name_plural = _(u'players')


class Coach(CTModel):
    """
    A Coach Entity
    """
    person = models.OneToOneField(Person, unique=True)
    coach_since = models.DateField(_(u'coach since'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.person

    class Meta:
        verbose_name = _(u'coach')
        verbose_name_plural = _(u'coaches')

        
# --------------------
# Team Models
# --------------------

class Team(CTModel):
    """
    A Team Entity
    """

    # FIXME
    # Not possible to be than one skip
    # - Check validation model and 'skip' method.

    name = models.CharField(_(u"name"), max_length=100)
    club = models.ForeignKey(Club, related_name="teams")
    coach = models.ForeignKey(Coach, related_name="teams", blank=True, null=True)
    players = models.ManyToManyField(Player, related_name="teams",
                                     through="TeamMembership")

    @property
    def members_list(self):
        return TeamMembership.objects.filter(team=self).order_by("-position")

    @property
    def skip(self):
        # Transform 'filter' in 'get'
        members_skip = self.members_list.filter(is_skip=True)
        if members_skip:
            return members_skip[0]
        return None

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'team')
        verbose_name_plural = _(u'teams')
        ordering = ('name',)


class TeamMembership(models.Model):
    """
    A Member Team Entity.
    """
    POSITION_CHOICES = (
        ("1", _(u"Lead")),
        ("2", _(u"Second")),
        ("3", _(u"Third")),
        ("4", _(u"Fourth")),
        ("0", _(u"Alternate"))
        )
    player = models.ForeignKey(Player, related_name="team_membership")
    team = models.ForeignKey(Team, related_name="team_membership")
    position = models.CharField(_("position"), max_length=1, choices=POSITION_CHOICES)
    is_vice = models.BooleanField(_("is vice ?"), default=False)
    is_skip = models.BooleanField(_("is skip ?"), default=False)

    def __unicode__(self):
        return u"%s - %s : %s" % (self.player, self.team, self.get_position_display())

    def clean(self):
        # Canot be both skip and vice.
        if self.is_skip and self.is_vice:
            raise ValidationError(_(u"A player can't be both vice and skip."))
    
    def get_absolute_url(self):
        return self.team.get_absolute_url()

    def get_absolute_list_url(self):
        return self.team.get_absolute_url()

    def get_absolute_edit_url(self):
        url_name = u'%s:%s%s' % (self.app_label, self.module_name, settings.URL_EDIT_SUFFIX)
        return reverse(url_name, args=[self.team.pk, self.pk])

    def get_absolute_delete_url(self):
        url_name = u'%s:%s%s' % (self.app_label, self.module_name, settings.URL_DELETE_SUFFIX)
        return reverse(url_name, args=[self.team.pk])

    class Meta:
        unique_together = ("player", "team")
        verbose_name = _(u"team member")
        verbose_name_plural = _(u"team members")
        ordering = ["team", "-position"]
