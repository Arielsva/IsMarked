import csv
from io import StringIO

from django.contrib.auth.models import User
from appointment.serializers import ProviderSerializer


def generate_provider_report_in_csv() -> StringIO:
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "provider",
        "customer_name",
        "customer_email",
        "customer_phone",
        "date_time",
        "active"
    ])

    providers = User.objects.all()
    serializer = ProviderSerializer(providers, many=True)

    for provider in serializer.data:
        appointments = provider["appointmets"]
        for appointment in appointments:
            writer.writerow(
                [
                    appointment["provider"],
                    appointment["customer_name"],
                    appointment["customer_email"],
                    appointment["customer_phone"],
                    appointment["date_time"],
                    appointment["active"]
                ]
            )

    return output