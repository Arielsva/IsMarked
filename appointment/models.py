from django.db import models

# Create your models here.

class Appointment(models.Model):
    provider = models.ForeignKey("auth.User", related_name="appointmets", on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    active = models.BooleanField(default=True)