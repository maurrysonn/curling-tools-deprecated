# -*- coding: utf-8 -*-
from curling_tools.core.forms import CTModelForm
from curling_tools.base.models import Person


class PersonForm(CTModelForm):

    class Meta:
        model = Person
        exclude = ('address',)
