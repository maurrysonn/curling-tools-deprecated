# -*- coding: utf-8 -*-
from django.contrib import admin
# Models module
from curling_tools.base.models import Country, City, Person

# Custom admin
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag')
    search_fields = ['name', 'code']

# Basics admin
admin.site.register(Country, CountryAdmin)
admin.site.register(City)
admin.site.register(Person)
