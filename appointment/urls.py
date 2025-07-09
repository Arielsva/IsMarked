from django.urls import path
from appointment.views import get_times, appointment_detail, AppointmentList, appointment_cancel

urlpatterns = [
    path('times/', get_times),
    path('appointment/', AppointmentList.as_view()),
    path('appointment/<int:pk>/', appointment_detail),
    path('appointment/cancel/<int:pk>/', appointment_cancel),
]