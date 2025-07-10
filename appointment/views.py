from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions

from datetime import datetime

from appointment.utils import get_available_times
from appointment.serializers import AppointmentSerializer, ProviderSerializer
from appointment.models import Appointment


class IsProviderOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        
        provider = request.query_params.get("provider", None)
        if request.user.username == provider:
            return True
        return False
    

class IsProvider(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.provider == request.user:
            return True
        return False


@api_view(http_method_names=["GET"])
def get_times(request):
    date = request.query_params.get('date')

    if not date:
        date = datetime.now().date()
    else:
        date = datetime.fromisoformat(date).date()

    available_times = sorted(list(get_available_times(date)))

    return JsonResponse(available_times, safe=False)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsProvider]
    
    
class AppointmentList(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsProviderOrCreateOnly]

    def get_queryset(self):
        provider = self.request.query_params.get("provider", None)
        queryset = Appointment.objects.filter(provider__username=provider)
        return queryset
    

@api_view(http_method_names=["POST"])
def appointment_cancel(request, pk):
    object = get_object_or_404(Appointment, id=pk)
    object.active = False
    object.save()
    return Response(status=200)


class ProviderList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [permissions.IsAdminUser]