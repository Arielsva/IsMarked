from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics

from datetime import datetime

from appointment.utils import get_available_times
from appointment.serializers import AppointmentSerializer
from appointment.models import Appointment


@api_view(http_method_names=["GET"])
def get_times(request):
    date = request.query_params.get('date')

    if not date:
        date = datetime.now().date()
    else:
        date = datetime.fromisoformat(date).date()

    available_times = sorted(list(get_available_times(date)))

    return JsonResponse(available_times, safe=False)

class AppointmentDetail(APIView):
    def get(self, request, pk):
        object = get_object_or_404(Appointment, id=pk)
        serializer = AppointmentSerializer(object)
        return JsonResponse(serializer.data)
    
    def patch(self, request, pk):
        object = get_object_or_404(Appointment, id=pk)
        serializer = AppointmentSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    def delete(self, request, pk):
        object = get_object_or_404(Appointment, id=pk)
        object.delete()
        return Response(status=204)
    
class AppointmentList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

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