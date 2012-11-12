# -*- coding: utf-8 -*-
from django.contrib import admin
# Models module
from curling_tools.base.models import *


# ----------------
# Geo Items Admins
# --------------------
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag')
    search_fields = ['name', 'code']

admin.site.register(Country, CountryAdmin)
admin.site.register(City)
admin.site.register(Address)

# -------------
# Clubs Admin
# -------------
admin.site.register(Club)

# -------------
# Places Admin
# -------------
admin.site.register(Rink)

# -------------
# Persons Admin
# -------------
admin.site.register(Person)
admin.site.register(Player)
admin.site.register(Coach)


# ----------
# Team Admin
# ----------
class TeamMemberInline(admin.TabularInline):
    model = TeamMembership

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline,]

admin.site.register(Team, TeamAdmin)
