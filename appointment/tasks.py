from drf.celery import app
from appointment.reports.reports_csv import generate_provider_report_in_csv
from appointment.services.email_service import send_mail_with_attachment


@app.task
def generate_providers_report(to_mail: list):
    report = generate_provider_report_in_csv()
    send_mail_with_attachment("DRF | IsMarked - Provider's report", to_mail, report, "providers_report.csv", "text/csv")