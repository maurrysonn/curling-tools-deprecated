# -*- coding: utf-8 -*-
from django import forms

from curling_tools.core.forms import CTModelForm
from curling_tools.base.models import (Person, Player, Coach,
                                       Club, Rink, Team, TeamMembership)


class PersonForm(CTModelForm):
    class Meta:
        model = Person
        exclude = ('address',)


class PersonPlayerForm(CTModelForm):
    class Meta:
        model = Player
        exclude = ('person',)


class PersonCoachForm(CTModelForm):
    class Meta:
        model = Coach
        exclude = ('person',)


class ClubForm(CTModelForm):
    class Meta:
        model = Club
        exclude = ('address',)


class RinkForm(CTModelForm):
    class Meta:
        model = Rink
        exclude = ('address',)


class TeamForm(CTModelForm):
    class Meta:
        model = Team
        exclude = ('players',)


class TeamMembershipForm(CTModelForm):
    class Meta:
        model = TeamMembership
        exclude = ('team',)


class TeamMembershipUpdateForm(CTModelForm):
    class Meta:
        model = TeamMembership
        widgets = {
            'team': forms.HiddenInput,
        }
