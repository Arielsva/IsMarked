from django.urls import path
from appointment.views import get_times, appointment_detail, appointment_list

urlpatterns = [
    path('times/', get_times),
    path('appointment/', appointment_list),
    path('appointment/<int:pk>/', appointment_detail),
]