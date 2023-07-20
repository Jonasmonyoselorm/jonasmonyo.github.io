from unicodedata import name
from django.db import models

from django.contrib.auth.models import User
from datetime import date


# Create your models here.

# TABLE VENUE


class Venue(models.Model):
    # Defining the columns of the table
    venue_name = models.CharField('Venue Name', max_length=120)
    veune_address = models.CharField(max_length=300)
    veune_zip_code = models.CharField('Zip Code', max_length=15)
    veune_phone = models.CharField(
        'Contact Phone', max_length=10, blank=True)
    veune_web = models.URLField('Website Address', blank=True)
    veune_email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        # Column to you see in admin db when you open the table
        return self.venue_name

# TABLE CLUB USERS


class MyClubUser(models.Model):
    # Defining the columns of the table
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_email = models.EmailField('User Email')

    def __str__(self):
        # Columns to you see in admin db when you open the table
        return self.first_name + ' ' + self.last_name

# TABLE EVENT


class Event(models.Model):
    # Definding the columns of the table
    event_name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    # USING FOREIGN KEY WITH VENUE TABLE (Venue)
    event_venue = models.ForeignKey(
        Venue, blank=True, null=True, on_delete=models.CASCADE)
    # event_venue = models.CharField('Event Venue', max_length=120)
    event_organizer = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    event_description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approveEvent = models.BooleanField("Approved Event", default=False)

    def __str__(self):
        return self.event_name  # Columns you see in admin db when you open the table

    # Calculating days left for Event
    @property
    def Days_till(self):
        today = date.today()
        daysTill = self.event_date.date() - today
        daysTillStripped = str(daysTill).split(",", 1)[0]
        return daysTillStripped

    @property
    def Is_Past(self):
        today = date.today()
        if self.event_date.date() <= today:
            event = "Past or It's today"
        else:
            event = "Future"
        return event
