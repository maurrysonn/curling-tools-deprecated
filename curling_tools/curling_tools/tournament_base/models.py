# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
# Curling Tools import
from curling_tools.core.models import CTModel
from curling_tools.core.exceptions import CTImproperlyConfigured
# -------------
# Global Models
# -------------

class SheetManager(models.Manager):
    
    def get_next(self, current_sheet=None):
        if current_sheet is None:
            next_order = 1
        else:
            next_order = current_sheet.order + 1
        next_sheet, created = self.get_or_create(order=next_order)
        return next_sheet

    def get_first(self):
        return self.get_next(current_sheet=None)

class Sheet(models.Model):
    """
    A sheet entity.

    A sheet is a place where a match is played (the playing surface).
    A rink is generally composed of 4, 6 or 8 sheets.
    """
    order = models.IntegerField(_(u"order"), default=1, unique=True)
    objects = SheetManager()

    @property
    def name(self):
        # TODO : custom displayed name
        # from settings (user or tournament rink).
        return self.order

    def __unicode__(self):
        return u'%s %s' % (_(u'Sheet'), self.name)

    def save(self, *args, **kwargs):
        # When adding a sheet,
        # the 'order' field is auto-incremented
        if not self.pk:
            try:
                last_order = Sheet.objects.order_by('-order')[0].order
            except IndexError:
                last_order = 0
            self.order = last_order+1
        return super(Sheet, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u"sheet")
        verbose_name_plural = _(u"sheets")
        ordering = ["order"]


class End(models.Model):
    """
    A end entity.
    
    A match is composed by many ends (genrally 8 or 10 ends).
    """
    order = models.IntegerField(_(u"order"), default=1, unique=True)

    def __unicode__(self):
        return u'%s' % self.order

    def save(self, *args, **kwargs):
        # When adding a end,
        # the 'order' field is auto-incremented
        if not self.pk:
            try:
                last_order = End.objects.order_by('-order')[0].order
            except IndexError:
                last_order = 0
            self.order = last_order+1
        return super(End, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u"end")
        verbose_name_plural = _(u"ends")
        ordering = ["order"]



# ----------------------
# Base Tournament Models
# ----------------------
# Will be define all basic abstract class like Tournament, TournamentRound, ...

# class Tournament(CTModel):
#     pass

# class TournamentRound(CTModel):
#     pass

# class Round(CTModel):
#     pass

# class Group(CTModel):
#     pass
