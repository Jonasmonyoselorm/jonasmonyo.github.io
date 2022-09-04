from unicodedata import name
from django.db import models

# Create your models here.

# TABLE VENUE

class Venue(models.Model):
    # Defining the columns of the table
    venue_name = models.CharField('Venue Name', max_length=120)
    veune_address = models.CharField(max_length=300)
    veune_zip_code = models.CharField('Zip Code', max_length=15)
    veune_phone = models.CharField('Contact Phone', max_length=10)
    veune_web = models.URLField('Website Address')
    veune_email_address = models.EmailField('Email Address')

    def __str__(self):
        return self.venue_name # Column to you see in admin db when you open the table

# TABLE CLUB USERS

class MyClubUser(models.Model):
    # Defining the columns of the table
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name # Columns to you see in admin db when you open the table

# TABLE EVENT

class Event(models.Model):
    # Definding the columns of the table
    event_name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    # USING FOREIGN KEY WITH VENUE TABLE (Venue)
    event_venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #event_venue = models.CharField('Event Venue', max_length=120)
    event_organizer = models.CharField(max_length=60)
    event_description = models.TextField(blank=True)

    attendees = models.ManyToManyField(MyClubUser, blank=True)


    def __str__(self):
        return self.event_name # Columns to you see in admin db when you open the table