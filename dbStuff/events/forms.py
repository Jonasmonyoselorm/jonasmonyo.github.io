from django import forms
# ModelForm needed cos we will add data to the models, helps add data into the DB
from django.forms import ModelForm
from .models import Venue, Event  # The TABLE to pull data from


# Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('venue_name', 'veune_address', 'veune_address', 'veune_web',
                  'veune_zip_code', 'veune_phone', 'veune_email_address', 'venue_image',)
        # "__all__"
        labels = {
            'venue_name': '',
            'veune_address': '',
            'veune_web': '',
            'veune_zip_code': '',
            'veune_phone': '',
            'veune_email_address': '',
            'venue_image': '',
        }
        widgets = {
            'venue_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Venue Name'}),
            'veune_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'veune_web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'veune_zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'veune_phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0243...'}),
            'veune_email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),

        }

# CREATE ADMIN SuperUser ADD_EVENT FORMS CLASS


class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_date', 'event_venue',
                  'event_organizer', 'attendees', 'event_description',)
        labels = {
            'event_name': '',
            'event_date': '',
            'event_venue': 'Venue',
            'event_organizer': 'Organizer',
            'attendees': 'Attendees',
            'event_description': '',
        }
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'event_venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'event_organizer': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Organizer'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# USERS ADD_EVENT FORM
class EventFormUsers(ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_date', 'event_venue',
                  'attendees', 'event_description')
        labels = {
            'event_name': '',
            'event_date': '',
            'event_venue': 'Venue',
            'attendees': 'Attendees',
            'event_description': '',
        }
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'event_venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
