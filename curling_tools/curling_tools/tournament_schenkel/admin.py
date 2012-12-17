# -*- coding: utf-8 -*-
from django.contrib import admin
# Models module
from curling_tools.tournament_schenkel.models import *

admin.site.register(SchenkelTournament)
admin.site.register(SchenkelRound)
admin.site.register(SchenkelGroup)
admin.site.register(SchenkelGroupRanking)

class ResultInlineAdmin(admin.TabularInline):
    model = SchenkelResult
    ordering = ('end',)

class MatchAdmin(admin.ModelAdmin):
    inlines = [ ResultInlineAdmin, ]
    
admin.site.register(SchenkelMatch, MatchAdmin)
