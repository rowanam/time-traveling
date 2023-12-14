from django.contrib import admin
from .models import Trip, Location

class LocationInlineAdmin(admin.StackedInline):
    model = Location
    extra = 0

class TripAdmin(admin.ModelAdmin):
    model = Trip
    inlines = [LocationInlineAdmin]

admin.site.register(Trip, TripAdmin)
