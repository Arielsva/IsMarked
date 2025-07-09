from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

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

@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def appointment_detail(request, pk):
    object = get_object_or_404(Appointment, id=pk)
    if request.method == "GET":
        serializer = AppointmentSerializer(object)
        return JsonResponse(serializer.data)
    if request.method == "PATCH":
        serializer = AppointmentSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "DELETE":
        object.delete()
        return Response(status=204)
    
class AppointmentList(APIView):
    def get(self, request):
        query = Appointment.objects.all()
        serializer = AppointmentSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        data = request.data
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@api_view(http_method_names=["POST"])
def appointment_cancel(request, pk):
    object = get_object_or_404(Appointment, id=pk)
    object.active = False
    object.save()
    return Response(status=200)