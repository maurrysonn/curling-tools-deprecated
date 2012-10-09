# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class Country(models.Model):
    "A basic country entity"

    name = models.CharField(_('name'), max_length=50, unique=True)
    short_name = models.CharField(_(u'short name'), max_length=5, blank=True)
    code = models.CharField(_('code'), max_length=5, unique=True)
    flag = models.CharField(_('flag'), max_length=100, blank=True)

    @property
    def flag_path(self):
        if self.flag:
            file_path = u'%s%s' % (self.flag, settings.FLAGS_COUNTRIES_EXT)
        else:
            file_path = u'%s%s' % (settings.DEFAULT_FLAG_COUNTRIES, settings.FLAGS_COUNTRIES_EXT)
        return os.path.join(settings.STATIC_FLAGS_COUNTRIES, file_path)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.code)

    class Meta:
        verbose_name = _(u'country')
        verbose_name_plural = _(u'countries')


class City(models.Model):
    "A basic city entity"

    name = models.CharField(_(u'name'), max_length=50)
    short_name = models.CharField(_(u'short name'), max_length=5, blank=True)
    default_zipcode = models.CharField(_(u'zipcode'), max_length=10, blank=True)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.country.name)

    class Meta:
        verbose_name = _(u'city')
        verbose_name_plural = _(u'cities')


class Address(models.Model):
    "A basic address informations"

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
        abstract = True
        verbose_name = _(u'address')
        verbose_name_plural = _(u'addresses')


class Person(Address):
    "A basic person entity"

    first_name = models.CharField(_(u'first name'), max_length=50)
    last_name = models.CharField(_(u'last name'), max_length=50)
    nickname = models.CharField(_(u'nickname'), max_length=50, blank=True)
    phone = models.CharField(_(u'phone'), max_length=20, blank=True)
    email = models.EmailField(_(u'email'), blank=True)
    dob = models.DateField(_(u'date of birth'), blank=True, null=True)
    # TODO : photo

    def __unicode__(self):
        return u'%s (%s)' % (self.first_name, self.last_name)

    class Meta:
        # FIXME
        #Abstract : If a personn is a player AND a coach, we
        # need to create 2 "person" entities
        # If not : we create a player an then re-use player
        # infos for creating a coach.
        # abstract = True
        verbose_name = _(u'person')
        verbose_name_plural = _(u'persons')
