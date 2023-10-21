from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy, reverse
from .models import *
from .utils import Calendar
from .forms import EventForm
import calendar
from django.db.models import Q
from django.views.generic import ListView
import logging
from django.utils import timezone
import json



class CalendarView(generic.ListView):
    model = Event
    template_name = 'app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # Pass the URLs for the previous and next months to the template
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        events = Event.objects.all()
        current_time = timezone.now()
        events_with_time_diff = []
        for event in events:
            event.start_time = timezone.localtime(event.start_time)
            time_diff = (event.start_time - current_time).total_seconds() / 60
            event_dict = {
                'event': event,
                'time_diff': time_diff if 0 <= time_diff <= 30 else None
            }
            events_with_time_diff.append(event_dict)

        context['events'] = events_with_time_diff

        return context


class EventMemberDeleteView(generic.DeleteView):
    model = Event
    template_name = "delete_event.html"
    success_url = reverse_lazy("app:calendar")

class EventListView(ListView):
    model = Event
    template_name = 'app/calendar.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        venue = self.request.GET.get('venue')
        sort = self.request.GET.get('sort')

        if location:
            print(f"Filtering by location: {location}")
            queryset = queryset.filter(location__iexact=location)

        if venue:
            print(f"Filtering by venue: {venue}")
            queryset = queryset.filter(venue__icontains=venue)

        if sort:
            if sort == 'date':
                queryset = queryset.order_by('start_time')
            elif sort == 'popularity':
                queryset = queryset.order_by('-popularity')
            elif sort == 'creation_time':
                queryset = queryset.order_by('creation_time')
        print("Filtered QuerySet:", queryset)

        return queryset



def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        # Extract the year and month from the request string
        parts = req_day.split('=')
        year, month = (int(x) for x in parts[1].split('-'))
        return date(year, month, day=1)
    return datetime.today()


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:calendar'))
    else:
        form = EventForm(instance=instance)

    logging.debug(f"Event object: {instance}")  # Log the event object

    context = {
        'form': form,
        'event': instance,  # Pass the event object to the context
    }

    return render(request, 'app/event.html', context)

def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("app:calendar"))
    return render(request, "event.html", {"form": form})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def all_events(request):
    events = Event.objects.all()

    # Handle form submission for filtering and sorting
    if request.method == 'GET':
        location = request.GET.get('location')
        venue = request.GET.get('venue')
        sort = request.GET.get('sort')

        if location:
            events = events.filter(location__icontains=location)

        if venue:
            events = events.filter(venue__icontains=venue)

        if sort:
            if sort == 'date':
                events = events.order_by('start_time')
            elif sort == 'popularity':
                events = events.order_by('-popularity')
            elif sort == 'creation_time':
                events = events.order_by('creation_time')

    current_time = timezone.now()

    for event in events:
        event.start_time = timezone.localtime(event.start_time)

    context = {'events': events, 'current_time': current_time}
    return render(request, 'all_events.html', context=context)

def events_list(request):
    events = Event.objects.all()
    events_data = []
    for event in events:
        events_data.append({
            'title': event.title,
            'description': event.description,
            'location': event.location,
            'venue': event.venue,
            'start_time': event.start_time,
            'popularity': event.popularity,
            'creation_time': event.creation_time
        })

    return JsonResponse(events_data, safe=False)

def subscribe(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.popularity += 1
        event.save()

    return render(request, 'event.html', {'event': event})