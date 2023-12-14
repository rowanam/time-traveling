from django.contrib import admin
from .models import CustomTrip, CustomLocation

class CustomLocationInlineAdmin(admin.StackedInline):
    model = CustomLocation
    extra = 0

class CustomTripAdmin(admin.ModelAdmin):
    model = CustomTrip
    inlines = [CustomLocationInlineAdmin]

admin.site.register(CustomTrip, CustomTripAdmin)
