# -*- coding: utf-8 -*-
from django.contrib import admin
# Models module
from curling_tools.tournament_schenkel.models import *

admin.site.register(SchenkelTournament)
admin.site.register(SchenkelTournamentRound)
admin.site.register(SchenkelGroup)
admin.site.register(SchenkelRound)

