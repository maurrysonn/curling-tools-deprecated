# -*- coding: utf-8 -*-
# Django import
from django.conf.urls import patterns, include, url
# CT import
from curling_tools.core.utils import get_default_model_url
# Module utils
from curling_tools.tournament_schenkel.utils import (PREFIX_URL_TOURNAMENT,
                                                     PREFIX_URL_MAIN_ROUND,
                                                     ST_get_default_model_url)
# Module views
from curling_tools.tournament_schenkel.views import (STSubmenu, STDashboardSubmenu,
                                                     STHomeView, STDashboardView,
                                                     STRoundListView, STRoundCreateView,
                                                     STRoundUpdateView, STRoundDetailView)
# Module forms
from curling_tools.tournament_schenkel.forms import (STTournamentRoundForm,
                                                     STGroupForm)
# Module models
from curling_tools.tournament_schenkel.models import (SchenkelTournament,
                                                      SchenkelGroup,
                                                      SchenkelTournamentRound,
                                                      SchenkelRound)


urlpatterns = patterns('',
                       # App Home View
                       url(r'^$', STHomeView.as_view(), name='home'),
                       )

# Tournament Urls
urlpatterns += get_default_model_url(SchenkelTournament, submenu_mixin=STSubmenu)

# Tournament Dashboard Url
urlpatterns += patterns('',
                        # Tournament Dashboard View
                        url(r'^%sdashboard/$' % PREFIX_URL_TOURNAMENT, STDashboardView.as_view(), name='dashboard'),
                        )

# Group Urls
urlpatterns += ST_get_default_model_url(SchenkelGroup,
                                        form_class=STGroupForm,
                                        submenu_mixin=STDashboardSubmenu)

# Tournament Round Urls
urlpatterns += ST_get_default_model_url(SchenkelTournamentRound,
                                        form_class=STTournamentRoundForm,
                                        submenu_mixin=STDashboardSubmenu)

# Round Urls
urlpatterns += ST_get_default_model_url(SchenkelRound,
                                        list_view=STRoundListView,
                                        creation_view=STRoundCreateView,
                                        update_view=STRoundUpdateView,
                                        detail_view=STRoundDetailView,
                                        prefix_pattern=PREFIX_URL_MAIN_ROUND,
                                        submenu_mixin=STDashboardSubmenu)
