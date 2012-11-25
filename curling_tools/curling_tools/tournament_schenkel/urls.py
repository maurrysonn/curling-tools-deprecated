# -*- coding: utf-8 -*-
# Django import
from django.conf.urls import patterns, include, url
# CT import
from curling_tools.core.utils import get_default_model_url
# Schenkel Tournament Utils
from curling_tools.tournament_schenkel.utils import PREFIX_URL_TOURNAMENT, ST_get_default_model_url
# Module views
from curling_tools.tournament_schenkel.views import (STSubmenu, STDashboardSubmenu,
                                                     STHomeView, STDashboardView,)
                                                     
from curling_tools.tournament_schenkel.forms import *
# Module models
from curling_tools.tournament_schenkel.models import (SchenkelTournament,
                                                      SchenkelGroup)


urlpatterns = patterns('',
                       # App Home View
                       url(r'^$', STHomeView.as_view(), name='home'),
                       )

urlpatterns += get_default_model_url(SchenkelTournament, submenu_mixin=STSubmenu)
urlpatterns += patterns('',
                        # Tournament Dashboard View
                        url(r'^%sdashboard/$' % PREFIX_URL_TOURNAMENT, STDashboardView.as_view(), name='dashboard'),
                        # url(r'^%sgroup/add/$' % PREFIX_URL_TOURNAMENT, STGroupCreateView.as_view(), name='group-add'),
                        # url(r'^%smain-round/add/$' % PREFIX_URL_TOURNAMENT, STTournamentRoundCreateView.as_view(), name='main-round-add'),
                        # url(r'^%smain-round/(?P<pk_main_round>\d+)/round/add/$' % PREFIX_URL_TOURNAMENT, STRoundCreateView.as_view(), name='round-add'),
                        )

urlpatterns += ST_get_default_model_url(SchenkelGroup, form_class=STGroupForm,
                                        submenu_mixin=STDashboardSubmenu)
urlpatterns += ST_get_default_model_url(SchenkelTournamentRound, form_class=STTournamentRoundForm,
                                        submenu_mixin=STDashboardSubmenu)
