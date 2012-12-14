# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('tournament_schenkel/scoring_board_tags/results.html', takes_context=True)
def show_results(context, team, match=None, results=None, nb_ends=None):
    try:
        # Get Match object
        if match is None:
            match = context['match']
        # Get nb of ends
        if nb_ends is None:
            nb_ends = context['ends'].count()
        # Get Results
        if results is None:
            results = context['results']
    except KeyError:
        return {}
    # Compute complete results
    total = 0
    last_end_order = 0
    if results:
        results_team = [None for i in range(1, nb_ends+1)]
        for result in results:
            last_end_order = result.end.order
            if result.team == team:
                scoring = result.scoring
                total += result.scoring
            else:
                scoring = 0
            results_team[result.end.order-1] = scoring
    else:
        results_team = [None for i in range(1, nb_ends+1)]
    # Update value '-1' for the current end
    if last_end_order < nb_ends and not match.finished:
        results_team[last_end_order] = -1
    # Get 'team_id' (team_1 or team_2 of match)
    # => Used by JS
    if team == match.team_1: team_id = 1
    else: team_id = 2
    return {'results': results_team,
            'total': total,
            'nb_ends': range(1, nb_ends+1),
            'match': match,
            'team': team,
            'team_id': team_id}
