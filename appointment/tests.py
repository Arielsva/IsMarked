import json
from datetime import date, datetime, timezone

from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from appointment.models import Appointment
from appointment.utils import get_available_times



def create_test_user(self):
    user = User.objects.create(email="test@email.com", username="test", password="test")
    self.client.force_authenticate(user)

class TestAvailabeTimes(TestCase):
    def test_available_times_today(self):
        data = get_available_times(date.today())

        assert type(data) == set
        assert data is not None

class TestAppointmentListing(APITestCase):
    def test_listing(self):
        create_test_user(self)
        response = self.client.get("/api/appointment/?provider=test")
        self.assertEqual(response.status_code, 200)

    def test_empty_listing(self):
        create_test_user(self)
        response = self.client.get("/api/appointment/?provider=test")
        data = json.loads(response.content)
        self.assertEqual(data, [])


class TestAppointmentCreation(APITestCase):
    def test_create_appointment(self):
        User.objects.create(email="test@email.com", username="test", password="test")

        appointment_request_data = {
            "provider": "test",
            "date_time": "2025-12-12T12:30:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 201)

        created_appointment = Appointment.objects.get()

        self.assertEqual(created_appointment.provider.username, "test")
        self.assertEqual(created_appointment.date_time, datetime(2025, 12, 12, hour=12, minute=30, second=0, tzinfo=timezone.utc))
        self.assertEqual(created_appointment.customer_name, "Test")
        self.assertEqual(created_appointment.customer_email, "test@email.com")
        self.assertEqual(created_appointment.customer_phone, "+550090000-0000")

    def test_create_appointment_with_invalid_provider_returns_400(self):
        appointment_request_data = {
            "provider": "test",
            "date_time": "2025-01-01T12:30:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_appointment_in_past_returns_400(self):
        User.objects.create(email="test@email.com", username="test", password="test")

        appointment_request_data = {
            "provider": "test",
            "date_time": "2025-01-01T12:30:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_appointment_in_invalid_time_returns_400(self):
        User.objects.create(email="test@email.com", username="test", password="test")

        appointment_request_data = {
            "provider": "test",
            "date_time": "2026-01-20T00:00:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 400)


class TestGetTimes(APITestCase):
    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
    def test_get_available_times_normal_day(self, _):
        response = self.client.get("/api/times/?date=2025-12-01")
        data = json.loads(response.content)
        self.assertNotEqual(data, [])
        self.assertEqual(datetime.fromisoformat(data[0]), datetime(2025, 12, 1, hour=9, minute=0, second=0, tzinfo=timezone.utc))
        self.assertEqual(datetime.fromisoformat(data[-1]), datetime(2025, 12, 1, hour=17, minute=30, second=0, tzinfo=timezone.utc))

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=True)
    def test_get_available_times_holiday_day_returns_empty_list(self, _):
        response = self.client.get("/api/times/?date=2025-01-01")
        data = json.loads(response.content)
        self.assertEqual(data, [])