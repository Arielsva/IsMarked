from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

from datetime import datetime

from appointment.utils import get_available_times


@api_view(http_method_names=["GET"])
def get_times(request):
    date =  request.query_params.get('date')

    if not date:
        date = datetime.now().date()
    else:
        date = datetime.fromisoformat(date).date()

    available_times = sorted(list(get_available_times(date)))

    return JsonResponse(available_times, safe=False)