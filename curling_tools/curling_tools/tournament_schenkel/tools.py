# -*- coding: utf-8 -*-
from django.db.models import Sum


class TeamResult(object):

    def __init__(self, **kwargs):
        if 'db_object' in kwargs:
            self._init_from_db_object(kwargs['db_object'])
        else:
            self._init_from_params(**kwargs)
            
    def _init_from_params(self, team=None,
                          rank=None, ex_aequo=False,
                          points=0, ends=0, stones=0,
                          ends_received=0, stones_received=0):
        self.rank = rank
        self.ex_aequo = ex_aequo
        self.team = team
        self.points = points
        self.ends = ends
        self.stones = stones
        self.ends_received = ends_received
        self.stones_received = stones_received

    def _init_from_db_object(self, obj):
        self._init_from_params(obj.team,
                               obj.rank, obj.ex_aequo,
                               obj.points, obj.ends, obj.stones,
                               obj.ends_received, obj.stones_received)

    def __cmp__(self, other):
        cmp_param_list = ['points', 'ends', 'stones']
        # If param are equal, we compare the next one
        for param in cmp_param_list:
            if getattr(self, param) != getattr(other, param):
                return cmp(getattr(self, param), getattr(other, param))
        # If still equal, we compare the lost ends (inverse comparaison).
        if self.ends_received != other.ends_received:
            return -cmp(self.ends_received, other.ends_received)
        # If still equal, we compare the stones received by team (inverse comparaison).
        return -cmp(self.stones_received, other.stones_received)

    def __add__(self, other):
        if other.team is not None and self.team != other.team:
            return
        self.rank = None
        self.ex_aequo = None
        self.points = self.points + other.points
        self.ends = self.ends + other.ends
        self.stones = self.stones + other.stones
        self.ends_received = self.ends_received + other.ends_received
        self.stones_received = self.stones_received + other.stones_received

    def __repr__(self, *args, **kwargs):
        if self.team is not None:
            name = self.team.name
        else:
            name = 'None'
        return u'%s : R:%s EA: %s P:%s E:%s S:%s ER:%s SR:%s' % (name, self.rank, self.ex_aequo,
                                                                 self.points, self.ends, self.stones,
                                                                 self.ends_received, self.stones_received)

def convert_ranking_db_to_team_results(ranking_db_list):
    """
    Convert a list of GroupRanking DB objects to a list of TeamResults objects.
    """
    return [TeamResult(db_object=obj) for obj in ranking_db_list]


def get_results_for_match(match):
    """
    Returns a dict with results of each team.

    Exemple: {'team_1': TeamResult, 'team_2': TeamResult}
    """
    # Results objects
    team_1 = TeamResult(team=match.team_1)
    team_2 = TeamResult(team=match.team_2)
    # Get all positive results for each team
    results_team_1 = match.results.filter(team=match.team_1).exclude(scoring=0)
    results_team_2 = match.results.filter(team=match.team_2).exclude(scoring=0)
    # Compute Stones
    team_1.stones = results_team_1.aggregate(Sum('scoring'))['scoring__sum']
    team_2.stones = results_team_2.aggregate(Sum('scoring'))['scoring__sum']
    # Compute Ends
    team_1.ends = results_team_1.count()
    team_2.ends = results_team_2.count()
    # Compute Points
    if team_1.stones > team_2.stones:
        team_1.points = 2
        team_2.points = 0
    elif team_1.stones < team_2.stones:
        team_1.points = 0
        team_2.points = 2
    else:
        team_1.points = 1
        team_2.points = 1
    # Compute Ends Received
    team_1.ends_received = team_2.ends
    team_2.ends_received = team_1.ends
    # Compute Stones Received
    team_1.stones_received = team_2.stones
    team_2.stones_received = team_1.stones
    # Return results
    return {'team_1': team_1, 'team_2': team_2}


def add_results_to_ranking(prev_ranking, results):
    """
    Add new results to existing ranking.
    """
    prev_ranking_decorated = {}
    for rank in prev_ranking:
        prev_ranking_decorated[rank.team] = rank
    results_decorated = {}
    for result in results:
        results_decorated[result.team] = result
    # Compute new results
    for team, result in results_decorated.items():
        prev_result = prev_ranking_decorated.get(team, None)
        if prev_result:
            result = result + prev_result
    # Return results
    return results_decorated.values()  

def compute_ranking(results_list):
    # Sort the list
    results_list.sort(reverse=True)
    # Upadte ranks and ex-aequo
    current_rank = 1
    equals_results = [results_list[0]]
    for result in results_list[1:]:
        if result == equals_results[0]:
            equals_results.append(result)
        else:
            for equal_result in equals_results:
                equal_result.rank = current_rank
                equal_result.ex_aequo = len(equals_results) > 1
            current_rank = current_rank + len(equals_results)
            equals_results = [result]
    # Treat last items
    for equal_result in equals_results:
        equal_result.rank = current_rank
        equal_result.ex_aequo = len(equals_results) > 1
    return results_list    
