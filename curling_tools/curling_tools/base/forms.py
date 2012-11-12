# -*- coding: utf-8 -*-
from curling_tools.core.forms import CTModelForm
from curling_tools.base.models import Person, Player


class PersonForm(CTModelForm):

    class Meta:
        model = Person
        exclude = ('address',)

class PersonPlayerForm(CTModelForm):

    # def __init__(self, args, **kwargs):
    #     self.person = kwargs['person']

    # def save(self, args, **kwargs):
    
    class Meta:
        model = Player
        exclude = ('person',)
