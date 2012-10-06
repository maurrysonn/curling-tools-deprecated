# -*- coding: utf-8 -*-
from django.contrib import admin
# Models module
from curling_tools.base.models import Country, City, Person


# Basics admin
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Person)
