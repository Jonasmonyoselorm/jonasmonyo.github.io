from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),

    # CREATE TEXT FILE
    path('venue_text', views.venue_text, name='venue-text'),
    # CREATE CSV FILE
    path('venue_csv', views.venue_csv, name='venue-csv'),
    # CREATE PDF FILE
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),

    # CREATE SEARCH VENUE
    path('search', views.search_venues, name='search-venue'),

    # CREATE SEARCH EVENT
    path('search_events', views.search_events, name='search-events'),

    # ADMIN DASHBOARD
    path('admin_dashboard', views.admin_dashboard, name='admin-dashboard'),

    # VENUE AND EVENTS
    # path('venue_event/<venue_id>', views.venue_event, name='venue-event'),

    # EVENT PATHs
    path('addevents/', views.add_events, name='add-events'),
    path('events/', views.all_events, name='list-events'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),

    # VENUE PATHs
    path('addvenue/', views.add_venue, name='add-venue'),
    path('list_venues/', views.list_venue, name='list-venue'),
    path('show_venue/<venue_id>', views.show_venues, name='show-venue'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),

    # MY EVENTS
    path('my_events', views.my_events, name='my-events'),


]
