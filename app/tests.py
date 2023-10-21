from django.test import TestCase
from django.utils import timezone
from .models import Event
from datetime import timedelta

class EventModelTestCase(TestCase):
    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            description="A test event",
            location="Test Location",
            venue="Test Venue",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            popularity=0
        )
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.description, "A test event")
        self.assertEqual(event.location, "Test Location")
        self.assertEqual(event.venue, "Test Venue")
        self.assertIsNotNone(event.start_time)
        self.assertIsNotNone(event.end_time)
        self.assertEqual(event.popularity, 0)

    def test_get_html_url(self):
        event = Event.objects.create(
            title="Test Event",
            description="A test event",
            location="Test Location",
            venue="Test Venue",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            popularity=0
        )
        html_url = event.get_html_url
        expected_url = f'<a href="/app/event_edit/{event.id}"> {event.title} </a>'
        self.assertNotEqual(html_url, expected_url)

    def test_time_diff(self):
        event = Event.objects.create(
            title="Test Event",
            description="A test event",
            location="Test Location",
            venue="Test Venue",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            popularity=0
        )
        time_difference = event.time_diff
        self.assertFalse(time_difference)
