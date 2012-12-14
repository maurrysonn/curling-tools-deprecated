# -*- coding: utf-8 -*-
# Django import
from django.conf.urls import patterns, include, url
# CT import
from curling_tools.core.utils import get_default_model_url
# Module utils
from curling_tools.tournament_schenkel.utils import (PREFIX_URL_TOURNAMENT,
                                                     PREFIX_URL_ROUND,
                                                     PREFIX_URL_GROUP,
                                                     ST_get_default_model_url)
# Module views
from curling_tools.tournament_schenkel.views import (STSubmenu, STDashboardSubmenu,
                                                     STHomeView, STDashboardView,
                                                     STGroupListView, STGroupCreateView,
                                                     STGroupUpdateView, STGroupDetailView,
                                                     STGroupStartMatchesView,
                                                     STGroupFinishMatchesView,
                                                     STGroupScoringBoardView,
                                                     STMatchScoreEndView,
                                                     STMatchFinishView,)
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
urlpatterns += patterns('',
                        # Start Matches View
                        url(r'^%sstart/$' % PREFIX_URL_GROUP,
                            STGroupStartMatchesView.as_view(),
                            name='schenkelgroup-start-matches'),
                        # Finish Group View
                        url(r'^%sfinish/$' % PREFIX_URL_GROUP,
                            STGroupFinishMatchesView.as_view(),
                            name='schenkelgroup-finish-matches'),
                        # Scoring Board View
                        url(r'^%sscoringboard/$' % PREFIX_URL_GROUP,
                            STGroupScoringBoardView.as_view(),
                            name='schenkelgroup-scoring-board'),
                        # Result of end
                        url(r'^scoring/end/$',
                            STMatchScoreEndView.as_view(),
                            name='match-scoring-end'),
                        # Finish Match
                        url(r'^match/finish/$',
                            STMatchFinishView.as_view(),
                            name='match-finish'),
                         )
