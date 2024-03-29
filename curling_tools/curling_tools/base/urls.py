# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from curling_tools.core.utils import get_default_model_url
# Module views
from curling_tools.base.views import (BaseSubmenu, BaseHomeView,
                                      PersonAddressUpdateView,
                                      PersonPlayerCreateView, PersonPlayerUpdateView,
                                      PersonCoachCreateView, PersonCoachUpdateView,
                                      ClubAddressUpdateView, RinkAddressUpdateView,
                                      TeamMembershipCreateView, TeamMembershipDeleteView,
                                      TeamMembershipUpdateView)
# Module models
from curling_tools.base.models import Country, City, Person, Club, Rink, Team
# Module forms
from curling_tools.base.forms import PersonForm, ClubForm, RinkForm, TeamForm


urlpatterns = patterns('',
                       # App Home View
                       url(r'^$', BaseHomeView.as_view(), name='home'),                       
                       )

# Models views
urlpatterns += get_default_model_url(Country, submenu_mixin=BaseSubmenu)
urlpatterns += get_default_model_url(City, submenu_mixin=BaseSubmenu)
urlpatterns += get_default_model_url(Person, submenu_mixin=BaseSubmenu, form_class=PersonForm)
urlpatterns += patterns('',
                        url(r'^person/(?P<pk>\d+)/address/edit/$',
                            PersonAddressUpdateView.as_view(),
                            name='person-address-edit'),
                        url(r'^person/(?P<pk>\d+)/player/add/$',
                            PersonPlayerCreateView.as_view(),
                            name='person-player-add'),
                        url(r'^person/(?P<pk>\d+)/player/edit/$',
                            PersonPlayerUpdateView.as_view(),
                            name='person-player-edit'),
                        url(r'^person/(?P<pk>\d+)/coach/add/$',
                            PersonCoachCreateView.as_view(),
                            name='person-coach-add'),
                        url(r'^person/(?P<pk>\d+)/coach/edit/$',
                            PersonCoachUpdateView.as_view(),
                            name='person-coach-edit'),
                        )
# urlpatterns += get_default_model_url(Player, submenu_mixin=BaseSubmenu)
urlpatterns += get_default_model_url(Club, submenu_mixin=BaseSubmenu, form_class=ClubForm)
urlpatterns += patterns('',
                        url(r'^club/(?P<pk>\d+)/address/edit/$',
                            ClubAddressUpdateView.as_view(),
                            name='club-address-edit'),
                        )

urlpatterns += get_default_model_url(Rink, submenu_mixin=BaseSubmenu, form_class=RinkForm)
urlpatterns += patterns('',
                        url(r'^rink/(?P<pk>\d+)/address/edit/$',
                            RinkAddressUpdateView.as_view(),
                            name='rink-address-edit'),
                        )

urlpatterns += get_default_model_url(Team, submenu_mixin=BaseSubmenu, form_class=TeamForm)
urlpatterns += patterns('',
                        url(r'^team/(?P<pk>\d+)/member/add/$',
                            TeamMembershipCreateView.as_view(),
                            name='teammembership-add'),
                        url(r'^team/(?P<pk_team>\d+)/member/(?P<pk>\d+)/delete/$',
                            TeamMembershipDeleteView.as_view(),
                            name='teammembership-delete'),
                        url(r'^team/(?P<pk_team>\d+)/member/(?P<pk>\d+)/edit/$',
                            TeamMembershipUpdateView.as_view(),
                            name='teammembership-edit'),
                        )
