from django.urls import path
from appointment.views import get_times, AppointmentDetail, AppointmentList, ProviderList, appointment_cancel

urlpatterns = [
    path('times/', get_times),
    path('appointment/', AppointmentList.as_view()),
    path('appointment/<int:pk>/', AppointmentDetail.as_view()),
    path('appointment/cancel/<int:pk>/', appointment_cancel),
    path('provider/', ProviderList.as_view()),
]