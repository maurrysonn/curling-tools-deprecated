# -*- coding: utf-8 -*-
from curling_tools.core.forms import CTModelForm
from curling_tools.base.models import Person, Player, Coach, Club, Rink


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

