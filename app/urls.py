from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>/', views.event, name='event_edit'),
    path(
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('all_events/', views.all_events, name='all_events'),
    path('events_list/', views.events_list, name='events_list'),
    path('subscribe/<int:event_id>/', views.subscribe, name='subscribe'),
]
