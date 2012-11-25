# -*- coding: utf-8 -*-
from django import forms

from curling_tools.core.forms import CTModelForm
from curling_tools.tournament_schenkel.models import (SchenkelGroup,
                                                     SchenkelTournamentRound,
                                                     SchenkelRound)

class STGroupForm(CTModelForm):
    class Meta:
        model = SchenkelGroup
        exclude = ('teams',)
        widgets = {'tournament': forms.HiddenInput}


class STTournamentRoundForm(CTModelForm):
    class Meta:
        model = SchenkelTournamentRound


class STRoundForm(CTModelForm):
    class Meta:
        model = SchenkelRound
