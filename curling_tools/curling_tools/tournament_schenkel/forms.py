# -*- coding: utf-8 -*-
from django import forms

from curling_tools.core.forms import CTModelForm
from curling_tools.tournament_schenkel.models import (SchenkelGroup,
                                                      SchenkelRound)


class STRoundForm(CTModelForm):
    class Meta:
        model = SchenkelRound
        widgets = {'tournament': forms.HiddenInput}


class STGroupForm(CTModelForm):
    class Meta:
        model = SchenkelGroup
        exclude = ('current', 'finished', 'order')
        widgets = {'round': forms.HiddenInput}
