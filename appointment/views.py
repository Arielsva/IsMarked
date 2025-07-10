from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, generics, permissions

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


class AppointmentDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsProvider]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class AppointmentList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = AppointmentSerializer
    permission_classes = [IsProviderOrCreateOnly]

    def get_queryset(self):
        provider = self.request.query_params.get("provider", None)
        queryset = Appointment.objects.filter(provider__username=provider)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

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