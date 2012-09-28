# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       # Main Homepage
                       url(r'^$', TemplateView.as_view(template_name="design/home.html"), name='home'),
                       # App Homepage
                       url(r'^app/$', TemplateView.as_view(template_name="design/app_home.html"), name='app-home'),
                       # List View
                       url(r'^list/$', TemplateView.as_view(template_name="design/list_view.html"), name='list'),
                       # Detail View
                       url(r'^list/$', TemplateView.as_view(template_name="design/detail_view.html"), name='detail'),
                       # Edit View
                       url(r'^list/$', TemplateView.as_view(template_name="design/edit_view.html"), name='edit'),
                       )
