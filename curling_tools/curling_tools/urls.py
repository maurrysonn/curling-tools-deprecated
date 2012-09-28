# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from curling_tools.core.views import TestView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'curling_tools.views.home', name='home'),
                       # url(r'^curling_tools/', include('curling_tools.foo.urls')),
                       
                       url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),

                       # Templates Interface designing
                       # url(r'^design/', include('curling_tools.design.urls', namespace='design')),

                       # Test Core Views
                       url(r'^test/view/$', TestView.as_view(),
                           name='test-view'),
                       url(r'^test/view/2/$', TestView.as_view(template_name='core/test/test_view.html'),
                           name='test-view-2'),

                       # Uncomment the admin/doc line below to enable admin documentation
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^_admin/', include(admin.site.urls)),
)
