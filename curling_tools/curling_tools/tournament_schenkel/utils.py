# -*- coding: utf-8 -*-
from curling_tools.core.utils import get_default_model_url
from curling_tools.tournament_schenkel.views import (STBaseListView,
                                                     STBaseCreateView,
                                                     STBaseDetailView,
                                                     STBaseUpdateView,
                                                     STBaseDeleteView)

PREFIX_URL_TOURNAMENT = 'tournament/(?P<pk_tournament>\d+)/'

def ST_get_default_model_url(*args, **kwargs):
    # Get specific Initial Data
    initial_params = {
        'prefix_pattern': PREFIX_URL_TOURNAMENT,
        'prefix_name': 'tournament-',
        'list_view': STBaseListView,
        'detail_view': STBaseDetailView,
        'creation_view': STBaseCreateView,
        'update_view': STBaseUpdateView,
        'delete_view': STBaseDeleteView}
    for param, value in initial_params.items():
        if param not in kwargs:
            kwargs[param] = value
    # Return result of the default function
    return get_default_model_url(*args, **kwargs)
