# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from curling_tools.core.utils import get_default_model_url
# Module views
from curling_tools.base.views import BaseSubmenu, BaseHomeView
# Module models
from curling_tools.base.models import Country, City, Person

urlpatterns = patterns('',
                       # App Home View
                       url(r'^$', BaseHomeView.as_view(), name='home'),
                       )

# Models views
urlpatterns += get_default_model_url(Country, submenu_mixin=BaseSubmenu)
urlpatterns += get_default_model_url(City, submenu_mixin=BaseSubmenu)
urlpatterns += get_default_model_url(Person, submenu_mixin=BaseSubmenu)
