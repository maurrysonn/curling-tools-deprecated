# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Module views
from curling_tools.base.views import CountryListView


urlpatterns = patterns('',
                       # Country views
                       url(r'^country/$', CountryListView.as_view(), name='country-list'),
                       )
