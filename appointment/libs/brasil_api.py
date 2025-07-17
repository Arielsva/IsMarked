import requests
from datetime import date


def is_holiday(date: date) -> bool:
    request = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{date.year}")

    if request.status_code != 200:
        ValueError("ERROR Brasil API")

    if date in [date.fromisoformat(_["date"]) for _ in request.json()]:
        return True
    return False