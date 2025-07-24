from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from appointment.models import Appointment
from appointment.utils import get_available_times


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields="__all__"

    provider = serializers.CharField()

    def validate_provider(self, value):
        try:
            provider_object = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("provider not found")
        return provider_object
    
    # TODO: Ajustar validação para filtrar horários por provider
    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("appointment cannot be done in the past")
        if value not in get_available_times(value.date()):
            raise serializers.ValidationError("schedule not available")
        return value
    

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "appointmets"]

    appointmets = AppointmentSerializer(many=True, read_only=True)