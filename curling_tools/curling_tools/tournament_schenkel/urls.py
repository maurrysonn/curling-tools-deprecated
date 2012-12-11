# -*- coding: utf-8 -*-
# Django import
from django.conf.urls import patterns, include, url
# CT import
from curling_tools.core.utils import get_default_model_url
# Module utils
from curling_tools.tournament_schenkel.utils import (PREFIX_URL_TOURNAMENT,
                                                     PREFIX_URL_ROUND,
                                                     ST_get_default_model_url)
# Module views
from curling_tools.tournament_schenkel.views import (STSubmenu, STDashboardSubmenu,
                                                     STHomeView, STDashboardView,
                                                     STGroupListView, STGroupCreateView,
                                                     STGroupUpdateView, STGroupDetailView
                                                     )
# Module forms
from curling_tools.tournament_schenkel.forms import (STRoundForm,
                                                     STGroupForm)
# Module models
from curling_tools.tournament_schenkel.models import (SchenkelTournament,
                                                      SchenkelRound,
                                                      SchenkelGroup)


urlpatterns = patterns('',
                       # App Home View
                       url(r'^$', STHomeView.as_view(), name='home'),
                       )

# Tournament Urls
urlpatterns += get_default_model_url(SchenkelTournament, submenu_mixin=STSubmenu)
urlpatterns += patterns('',
                        # Dashboard View
                        url(r'^%sdashboard/$' % PREFIX_URL_TOURNAMENT, STDashboardView.as_view(), name='dashboard'),
                        )

# Round Urls
urlpatterns += ST_get_default_model_url(SchenkelRound,
                                        form_class=STRoundForm,
                                        submenu_mixin=STDashboardSubmenu)

# Group Urls
urlpatterns += ST_get_default_model_url(SchenkelGroup,
                                        list_view=STGroupListView,
                                        creation_view=STGroupCreateView,
                                        update_view=STGroupUpdateView,
                                        detail_view=STGroupDetailView,
                                        prefix_pattern=PREFIX_URL_ROUND,
                                        submenu_mixin=STDashboardSubmenu)
