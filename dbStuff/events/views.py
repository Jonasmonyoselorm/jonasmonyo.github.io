from django.shortcuts import render
# working with calender
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# to redicrect to different page
from django.http import HttpResponseRedirect
# Import all DBs tables
from .models import Event, Venue
# Import USER model
from django.contrib.auth.models import User
# Import forms from "forms.py"
from .forms import VenueForm, EventFormUsers, EventFormAdmin
# to diplay message on pages
from django.contrib import messages
# to help generate text file
from django.http import HttpResponse
# to help generate csv files
import csv
# FOR PDF IMPORT ALL
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator


# Create your views here.

# hompage and calender
def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Monyo"

    month = month.capitalize()  # convert case to initial case letters

    # Convert month name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )

    # Get current year and date
    timeNow = datetime.now()
    current_year = timeNow.year

    # Query the Event Modal for Dates
    EventInMonth = Event.objects.filter(
        event_date__year=year,
        # Assign the month number, you can enter the month number (1,2,3,4,...12)
        event_date__month=month_number,
    )

    # Get current time

    # READ datetime @ gooogle, python datetime
    time = timeNow.strftime('%D %I:%M:%S %A')

    return render(request, 'index.html', {
        "last_name": name,
        "year": year,
        "month": month,
        "mon_number": month_number,
        "calender": cal,
        "currentYear": current_year,
        "currentTime": time,
        "AllEventInMonth": EventInMonth,
    })

# ADMIN DASHBOARD


def admin_dashboard(request):
    # fetch all venue
    vennueWithEvent = Venue.objects.all()

    # count the total in database
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_connt = User.objects.all().count()

    # update approvals in Database
    allEventToApprove = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('approvedCheckboxes')

            # uncheck all events
            allEventToApprove.update(approveEvent=False)

            # update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(
                    approveEvent=True)  # convert the pk to integer first

            messages.success(request, ("Events approval has been updated"))
            return HttpResponseRedirect('/events')
        else:
            return render(request, 'event/admin_approval.html', {
                'allEventToApprove': allEventToApprove,
                'totalEvents': event_count,
                'totalVenue': venue_count,
                'totalUsers': user_connt,
                'vennueWithEvent': vennueWithEvent,
            })
    else:
        messages.success(
            request, ("You are not authorized to view this page..."))
        return HttpResponseRedirect('/')

# Venue and Event page


def venue_event(request, venue_id):
    # Grab the venue
    venueWanted = Venue.objects.get(id=venue_id)
    # Grab the events for the venueWanted
    showEvents = venueWanted.event_set.all()

    if showEvents:
        return render(request, 'event/venue_and_event.html', {
            'showEvents': showEvents,
        })
    else:
        messages.success(request, ("No Events available..."))
        return HttpResponseRedirect('event/admin_dashboard')


# MY EVENTS
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me).order_by('event_date')
        return render(request, 'event/my_events.html', {
            'my_eventsEvents': events,
        })
    else:
        messages.success(request, ("You are not authorized view this page..."))
        return HttpResponseRedirect('/')
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
        # adding DB columns to the csv filegit
        csvWriter.writerow(
            [venue.venue_name, venue.veune_address, venue.veune_zip_code, venue.veune_phone, venue.veune_web, venue.veune_email_address])

    return textResonse

# GENERATE A TEXT FILE
# befor you begin, install reportLab in the terminal (pip install)


def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    #  Add some lines of text
    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    #     "This is line 4",
    # ]

    # Designate the VENUE Model
    venueToPdf = Venue.objects.all()

    # Create blank list
    line = []

    for venue in venueToPdf:
        line.append(venue.venue_name)
        line.append(venue.veune_address)
        line.append(venue.veune_zip_code)
        line.append(venue.veune_phone)
        line.append(venue.veune_web)
        line.append(venue.veune_email_address)
        line.append("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    # Loop
    for line in line:
        textob.textLine(line)

    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# ADD SEARCH VENUE BUTTON ON PAGE


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

# ADD SEARCH EVENTS ON PAGE


def search_events(request):
    if request.method == "POST":
        # receiving word from the search input
        searchedWord = request.POST['searched']
        # make search by venue_name in the model
        SearchEvent = Event.objects.filter(event_name__contains=searchedWord)

        return render(request, 'event/search_events.html', {
            'searchedWord': searchedWord,
            'SearchEvent': SearchEvent
        })
    else:
        return render(request, 'event/search_events.html', {})


# EVENTS SECTION VIEW
# Selecting from the Event TABLE IN DATABASE

# ADDING EVENTS INTO THE DB
def add_events(request):
    submitted = False
    if request.method == "POST":
        # if request.user.id == 4:
        if request.user.is_superuser:
            addEventForm = EventFormAdmin(request.POST)

            # form validation
            if addEventForm.is_valid():
                addEventForm.save()
                return HttpResponseRedirect('/addevents')
        else:
            addEventForm = EventFormUsers(request.POST)

            # form validation
            if addEventForm.is_valid():
                # addEventForm.save()

                event = addEventForm.save(commit=False)
                event.event_organizer = request.user  # linking to logged-in-user "request.user"
                event.save()
                return HttpResponseRedirect('/addevents')
    else:
        # just load the page when visited
        if request.user.is_superuser:
            addEventForm = EventFormAdmin
        else:
            addEventForm = EventFormUsers

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
    # Check which user form to display by user
    if request.user.is_superuser:
        EventFormToUpdate = EventFormAdmin(
            request.POST or None, instance=eventToUpdate)
    else:
        EventFormToUpdate = EventFormUsers(
            request.POST or None, instance=eventToUpdate)

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
    if request.user == eventToDelete.event_organizer:
        eventToDelete.delete()
        messages.success(request, ("Event Deleted"))
        return HttpResponseRedirect('/events')
    else:
        messages.success(request, ("You are not authorized to do that"))
        return HttpResponseRedirect('/events')


# VENUE SECTION VIEW
# ADDIND VENUE INTO THE DB


def add_venue(request):
    submitted = False

    if request.method == "POST":
        # RECEIVING FORM FIELDS
        addVenueForm = VenueForm(request.POST, request.FILES)
        if addVenueForm.is_valid():
            venue = addVenueForm.save(commit=False)
            venue.owner = request.user.id  # linking to logged-in-user
            venue.save()
            # addVenueForm.save()
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

    # Set up Paginatoion
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venuePagination = p.get_page(page)
    # multiply each number by a sting "a"
    nums = "a" * venuePagination.paginator.num_pages

    return render(request, 'venue/venue_lists.html', {
        'VenueList': VenueList,  # to output the query result on the page
        'venuePagination': venuePagination,  # output query by paginations
        'showNums': nums  # to pass the page numbers on the page
    })

# view venues in a separet page


def show_venues(request, venue_id):
    ShowVenue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=ShowVenue.owner)

    return render(request, 'venue/show_venue.html', {
        'ShowVenue': ShowVenue,
        'venue_owner': venue_owner,
    })


# UPDATE / EDITING RECORD

def update_venue(request, venue_id):
    venueToUpdate = Venue.objects.get(pk=venue_id)
    VenueFormToUpdate = VenueForm(
        request.POST or None, request.FILES or None, instance=venueToUpdate)
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


# PYTHON DIAMOND PATTERN

def python_diamond_pattern():
    rows = 8

    # upper pyramid
    for i in range(1, rows):
        for j in range(1, rows - i):
            print(' ', end='')
        for j in range(0, 2 * i - 1):
            print('*', end='')
        print()

    # lower pyramid
    for i in range(rows - 2, 0, -1):
        for j in range(1, rows - i):
            print(' ', end='')
        for j in range(1, 2 * i):
            print('*', end='')
        print()
