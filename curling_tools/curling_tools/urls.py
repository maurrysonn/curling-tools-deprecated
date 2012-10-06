# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       # Homepage
                       url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),

                       # Base module
                       url(r'^base/', include('curling_tools.base.urls', namespace='base')),

                       # Templates Interface designing
                       # url(r'^design/', include('curling_tools.design.urls', namespace='design')),

                       # Test Core Views
                       # url(r'^test/view/$', TestView.as_view(), name='test-view'),
                       # url(r'^test/view/2/$', TestView.as_view(), name='test-view-2'),
                       # url(r'^test/view/list/$', TestListView.as_view(), name='test-list'),

                       # Uncomment the admin/doc line below to enable admin documentation
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^_admin/', include(admin.site.urls)),
                       )
