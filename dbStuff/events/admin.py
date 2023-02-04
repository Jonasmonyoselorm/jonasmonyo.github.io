from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event


# Register your models here.


# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)


# USE THIS TO DISPLAY SPECIFIC COLUMNS IN THE DB
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'veune_address',
                    'veune_phone')  # columns to display
    # TO arrange the list in A-z, use "-venue_name" to invert from z-A
    ordering = ('venue_name',)
    # TO add SEARCH bar in the Table side
    search_fields = ('venue_name', 'veune_address')

# USE THIS TO DISPLAY COLUMNS IN GROUPS AND FILTER IN THE DB


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('event_name', 'event_venue'), 'event_date',
              'event_description', 'event_organizer')
    list_display = ('event_name', 'event_date', 'event_venue')
    list_filter = ('event_date', 'event_venue')
    ordering = ('event_date',)
