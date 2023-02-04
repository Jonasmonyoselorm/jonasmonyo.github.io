from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm

from django.http import HttpResponse  # to help generate text file
import csv  # to help generate csv files

# Create your views here.

# hompage


def index(request):
    return render(request, 'index.html', {})

# GENERATE A TEXT FILE


def venue_text(request):
    textResonse = HttpResponse(content_type='text/plain')
    textResonse['Content-Disposition'] = 'attachment; filename=venues.txt'

    # Designate The Venue Model
    venueTextOutput = Venue.objects.all()

    # Create blank list
    lines = []
    # Loop Through and Output
    for venue in venueTextOutput:
        # adding DB columns to the text file
        lines.append(
            f'{venue.venue_name}\n{venue.veune_address}\n{venue.veune_zip_code}\n{venue.veune_phone}\n{venue.veune_web}\n{venue.veune_email_address}\n\n\n\n')

    # lines = ["This is line 1\n",
    #          "This is line 2\n",
    #          "This is line 3\n",
    #          "This is line 4\n\n",

    #          "Jonas is Awesome\n\n",
    #          ]

    # Write to TextFile
    textResonse.writelines(lines)
    return textResonse

# GENERATE A CSV / EXCEL FILE


def venue_csv(request):
    textResonse = HttpResponse(content_type='text/csv')
    textResonse['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Creating a csv writer
    csvWriter = csv.writer(textResonse)

    # Designate The Venue Model
    venueTextOutput = Venue.objects.all()

    # add columns to csv file
    csvWriter.writerow(['Venue Name', 'Address', 'Zip Code',
                       'Phone Numbers', 'Website', 'Email'])

    # Loop Through and Output
    for venue in venueTextOutput:
        # adding DB columns to the csv file
        csvWriter.writerow(
            [venue.venue_name, venue.veune_address, venue.veune_zip_code, venue.veune_phone, venue.veune_web, venue.veune_email_address])

    return textResonse

# ADD SEARCH BUTTON ON PAGE


def search_venues(request):
    if request.method == "POST":
        # receiving word from the search input
        searchedWord = request.POST['searched']
        # make search by venue_name in the model
        SearchVenue = Venue.objects.filter(venue_name__contains=searchedWord)

        return render(request, 'venue/search_venues.html', {
            'searchedWord': searchedWord,
            'SearchVenue': SearchVenue
        })
    else:
        return render(request, 'venue/search_venues.html', {})


# EVENTS SECTION VIEW
# Selecting from the Event TABLE IN DATABASE

# ADDING EVENTS INTO THE DB
def add_events(request):
    submitted = False
    if request.method == "POST":
        addEventForm = EventForm(request.POST)
        if addEventForm.is_valid():
            addEventForm.save()
            return HttpResponseRedirect('/addevents')
    else:
        addEventForm = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'event/add_events.html', {
        'submitted': submitted,
        'addEventForm': addEventForm,
    })

# LISTING ALL EVENTS


def all_events(request):

    # selecting all columns from the Event tables
    # use '?' in .order_by to make list random when page loads
    events_list = Event.objects.all().order_by('event_date')

    return render(request, 'event/event_lists.html', {
        'eventsList': events_list
    })

# UPDATE / EDIT EVENTS


def update_event(request, event_id):
    eventToUpdate = Event.objects.get(pk=event_id)
    EventFormToUpdate = EventForm(request.POST or None, instance=eventToUpdate)
    if EventFormToUpdate.is_valid():
        EventFormToUpdate.save()
        return HttpResponseRedirect('/events')

    return render(request, 'event/update_event.html', {
        'eventToUpdate': eventToUpdate,
        'eventFormToUpdate': EventFormToUpdate
    })

# DELETE EVENT


def delete_event(request, event_id):
    eventToDelete = Event.objects.get(pk=event_id)
    eventToDelete.delete()
    return HttpResponseRedirect('/events')


# VENUE SECTION VIEW
# ADDIND VENUE INTO THE DB


def add_venue(request):
    submitted = False

    if request.method == "POST":
        addVenueForm = VenueForm(request.POST)  # RECEIVING FORM FIELDS
        if addVenueForm.is_valid():
            addVenueForm.save()
            return HttpResponseRedirect('/addvenue?submitted=True')
    else:
        addVenueForm = VenueForm  # RECEIVING FORM FIELDS
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'venue/add_venue.html', {
        'addVenueForm': addVenueForm,
        'submitted': submitted,
    })


# CREATING ALL LIST OF VENUES

def list_venue(request):

    # selecting all columns from the Venue tables
    # use '?' in .order_by to make list random when page loads
    VenueList = Venue.objects.all().order_by('venue_name')

    return render(request, 'venue/venue_lists.html', {
        'VenueList': VenueList
    })

# view venues in a separet page


def show_venues(request, venue_id):
    ShowVenue = Venue.objects.get(pk=venue_id)
    return render(request, 'venue/show_venue.html', {
        'ShowVenue': ShowVenue
    })


# UPDATE / EDITING RECORD

def update_venue(request, venue_id):
    venueToUpdate = Venue.objects.get(pk=venue_id)
    VenueFormToUpdate = VenueForm(request.POST or None, instance=venueToUpdate)
    if VenueFormToUpdate.is_valid():
        VenueFormToUpdate.save()
        return HttpResponseRedirect('/list_venues')

    return render(request, 'venue/update_venue.html', {
        'venueToUpdate': venueToUpdate,
        'VenueFormToUpdate': VenueFormToUpdate
    })

# DELETE VENUE


def delete_venue(request, venue_id):
    venueToDelet = Venue.objects.get(pk=venue_id)
    venueToDelet.delete()
    return HttpResponseRedirect('/list_venues')
