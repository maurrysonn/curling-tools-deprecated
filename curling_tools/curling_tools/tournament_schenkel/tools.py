# -*- coding: utf-8 -*-
from django.db.models import Sum


def get_complete_results_for_match(match):
    """
    Returns a dict with all results of the match.

    Exemple: {'team_1':
                 {'points': 2, 'ends': 6, 'stones': 10, 'ends_received': 2, stones_received': 3},
              'team_2':
                 {'points': 0, 'ends': 2, 'stones': 3, 'ends_received': 6, stones_received': 10}}
    """
    global_results = {'team_1': {'team': match.team_1}, 'team_2': {'team': match.team_2}}
    # Get all positive results for each team
    results_team_1 = match.results.filter(team=match.team_1).exclude(scoring=0)
    results_team_2 = match.results.filter(team=match.team_2).exclude(scoring=0)
    # Compute Stones
    global_results['team_1']['stones'] = results_team_1.aggregate(Sum('scoring'))['scoring__sum']
    global_results['team_2']['stones'] = results_team_2.aggregate(Sum('scoring'))['scoring__sum']
    # Compute Ends
    global_results['team_1']['ends'] = results_team_1.count()
    global_results['team_2']['ends'] = results_team_2.count()
    # Compute Points
    if global_results['team_1']['stones'] > global_results['team_2']['stones']:
        global_results['team_1']['points'] = 2
        global_results['team_2']['points'] = 0
    elif global_results['team_1']['stones'] < global_results['team_2']['stones']:
        global_results['team_1']['points'] = 0
        global_results['team_2']['points'] = 2
    else:
        global_results['team_1']['points'] = 1
        global_results['team_2']['points'] = 1
    # Compute Ends Received
    global_results['team_1']['ends_received'] = global_results['team_2']['ends']
    global_results['team_2']['ends_received'] = global_results['team_1']['ends']
    # Compute Stones Received
    global_results['team_1']['stones_received'] = global_results['team_2']['stones']
    global_results['team_2']['stones_received'] = global_results['team_1']['stones']
    # Return results
    return global_results


def cmp_result():
    pass


def compute_ranking(match_results):
    ranking_list = []
    for result in match_results:
        for team_key in ['team_1', 'team_2']:
            ranking_list.append(result[team_key])
    # Sort list
    
    return ranking_list
    
