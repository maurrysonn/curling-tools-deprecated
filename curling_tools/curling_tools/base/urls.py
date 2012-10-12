# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Module views
from curling_tools.base.views import BaseHome, CountryListView, CountryDetailView


urlpatterns = patterns('',
                       url(r'^$', BaseHome.as_view(), name='dashboard'),
                       # Country views
                       url(r'^country/$', CountryListView.as_view(), name='country-list'),
                       url(r'^country/(?P<pk>\d+)/$', CountryDetailView.as_view(), name='country-detail'),
                       )
