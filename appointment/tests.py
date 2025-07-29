import json
from datetime import date, datetime, timezone

from unittest import mock
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from appointment.models import Appointment
from appointment.utils import get_available_times


class TestAppointmentListing(APITestCase):
    def test_listing(self):
        user = User.objects.create(email="test@email.com", username="test", password="test")
        self.client.force_authenticate(user)
        response = self.client.get("/api/appointment/?provider=test")
        self.assertEqual(response.status_code, 200)

    def test_empty_listing(self):
        user = User.objects.create(email="test@email.com", username="test", password="test")
        self.client.force_authenticate(user)
        response = self.client.get("/api/appointment/?provider=test")
        data = json.loads(response.content)
        self.assertEqual(data, [])


class TestAppointmentCreation(APITestCase):
    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
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

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
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

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
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

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
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

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
    def test_create_appointment_at_scheduled_time_returns_400(self, _):
        User.objects.create(email="test@email.com", username="test", password="test")

        appointment_request_data_1 = {
            "provider": "test",
            "date_time": "2026-07-28T09:00:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response_1 = self.client.post("/api/appointment/", appointment_request_data_1, format="json")
        self.assertEqual(response_1.status_code, 201)

        appointment_request_data_2 = {
            "provider": "test",
            "date_time": "2026-07-28T09:00:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response_2 = self.client.post("/api/appointment/", appointment_request_data_2, format="json")
        self.assertEqual(response_2.status_code, 400)
        
    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)    
    def test_create_appointment_at_scheduled_time_for_another_provider_returns_200(self, _):
        User.objects.create(email="test@email.com", username="test", password="test")
        User.objects.create(email="admin@email.com", username="admin", password="admin")

        appointment_request_data_test = {
            "provider": "test",
            "date_time": "2026-07-28T09:00:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response_test = self.client.post("/api/appointment/", appointment_request_data_test, format="json")
        self.assertEqual(response_test.status_code, 201)

        appointment_request_data_admin = {
            "provider": "admin",
            "date_time": "2026-07-28T09:00:00Z",
            "customer_name": "Admin",
            "customer_email": "admin@email.com",
            "customer_phone": "+550090000-0000"
        }

        response_admin = self.client.post("/api/appointment/", appointment_request_data_admin, format="json")
        self.assertEqual(response_admin.status_code, 201)


class TestGetTimes(APITestCase):
    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
    def test_available_times_today(self, _):
        data = get_available_times(date.today())
        assert type(data) == set
        assert data is not None

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


class TestProviderListing(APITestCase):
    def test_not_admin_listing_providers_returns_403(self):
        response = self.client.get("/api/provider/")
        self.assertEqual(response.status_code, 403)

    @mock.patch("appointment.libs.brasil_api.is_holiday", return_value=False)
    def test_admin_listing_providers_returns_list(self):
        User.objects.create(email="test@email.com", username="test", password="test")
        user = User.objects.create(email="admin@email.com", username="admin", password="admin", is_staff=True)
        self.client.force_authenticate(user)

        appointment_request_data = {
            "provider": "test",
            "date_time": "2026-01-20T09:00:00Z",
            "customer_name": "Test",
            "customer_email": "test@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 201)

        appointment_request_data = {
            "provider": "admin",
            "date_time": "2026-01-20T17:30:00Z",
            "customer_name": "Admin",
            "customer_email": "admin@email.com",
            "customer_phone": "+550090000-0000"
        }

        response = self.client.post("/api/appointment/", appointment_request_data, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/provider/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response, [])