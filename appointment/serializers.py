from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from appointment.models import Appointment
from appointment.utils import get_available_times


class AppointmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=0)
    provider = serializers.CharField()
    date_time = serializers.DateTimeField()
    customer_name = serializers.CharField(max_length=200)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    active = serializers.BooleanField(default=True)

    def validate_provider(self, value):
        try:
            provider_object = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("provider not found")
        return provider_object
    
    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("appointment cannot be done in the past")
        if value not in get_available_times(value.date()):
            raise serializers.ValidationError("schedule not available")
        return value

    def create(self, validated_data):
        appointment = Appointment.objects.create(
            provider = validated_data["provider"],
            date_time = validated_data["date_time"],
            customer_name = validated_data["customer_name"],
            customer_email = validated_data["customer_email"],
            customer_phone = validated_data["customer_phone"]
        )
        return appointment
    
    def update(self, instance, validated_data):
        instance.date_time = validated_data.get("date_time", instance.date_time)
        instance.customer_name = validated_data.get("customer_name", instance.customer_name)
        instance.customer_email = validated_data.get("customer_email", instance.customer_email)
        instance.customer_phone = validated_data.get("customer_phone", instance.customer_phone)
        instance.save()
        return instance