from re import M
from django.shortcuts import render

import calendar
from calendar import HTMLCalendar
from datetime import datetime

# Create your views here.


def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Monyo"

    month = month.capitalize() # convert case to initial case letters

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
    
    # Get current time

    time = timeNow.strftime('%D %I:%M:%S %A') # READ datetime @ gooogle, python datetime

    return render(request, 'index.html', {
        "last_name" : name,
        "year": year,
        "month": month,
        "mon_number": month_number, 
        "calender": cal,
        "currentYear": current_year,
        "currentTime": time,
    })