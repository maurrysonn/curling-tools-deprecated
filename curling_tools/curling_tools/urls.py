# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       # Homepage
                       url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),
                       # Base module
                       url(r'^base/', include('curling_tools.base.urls', namespace='base')),
                       # Design module
                       url(r'^design/', include('curling_tools.design.urls', namespace='design')),

                       # url(r'^_admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^_admin/', include(admin.site.urls)),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^medias/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            )
