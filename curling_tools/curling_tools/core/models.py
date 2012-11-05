# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class CTModel(models.Model):
    
    @property
    def app_label(self):
        return self._meta.app_label

    @property
    def module_name(self):
        return self._meta.module_name

    def get_absolute_url(self):
        url_name = u'%s:%s%s' % (self.app_label, self.module_name, settings.URL_DETAIL_SUFFIX)
        return reverse(url_name, args=[self.pk])

    def get_absolute_edit_url(self):
        url_name = u'%s:%s%s' % (self.app_label, self.module_name, settings.URL_EDIT_SUFFIX)
        return reverse(url_name, args=[self.pk])

    def get_absolute_delete_url(self):
        url_name = u'%s:%s%s' % (self.app_label, self.module_name, settings.URL_DELETE_SUFFIX)
        return reverse(url_name, args=[self.pk])

    class Meta:
        abstract = True
