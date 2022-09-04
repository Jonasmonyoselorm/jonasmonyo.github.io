from django.shortcuts import render
from .models import Event

# Create your views here.

def index(request):
    return render(request, 'index.html', {})


# Selecting from the Event TABLE IN DATABASE
def all_events(request):
    events_list = Event.objects.all()
    return render(request, 'event_lists.html', {
        'eventsList' : events_list
    })

