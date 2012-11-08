# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from curling_tools.core.models import CTModel

# ------------------
# Statics Ressources
# ------------------
STATIC_FLAGS_COUNTRIES = 'base/images/flags'
FLAGS_COUNTRIES_EXT = '.png'
DEFAULT_FLAG_COUNTRIES = 'default'

class Country(CTModel):
    "A basic country entity"

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
        ordering = ('name',)


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
        verbose_name = _(u'address')
        verbose_name_plural = _(u'addresses')


class Person(CTModel):
    "A basic person entity"

    first_name = models.CharField(_(u'first name'), max_length=50)
    last_name = models.CharField(_(u'last name'), max_length=50)
    nickname = models.CharField(_(u'nickname'), max_length=50, blank=True)
    phone = models.CharField(_(u'phone'), max_length=20, blank=True)
    mobile_phone = models.CharField(_(u'mobile phone'), max_length=20, blank=True)
    email = models.EmailField(_(u'email'), blank=True)
    dob = models.DateField(_(u'date of birth'), blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True)
    photo = models.ImageField(_(u'photo'), upload_to='base/person', max_length=200, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = _(u'person')
        verbose_name_plural = _(u'persons')
        ordering = ('last_name', 'first_name')
