from clients.http import NotFoundError, ServiceError, get_with_retry, parse_json, require

BASE_URL = "https://api.frankfurter.dev/v2"


def get_rate(currency="USD"):
    response = get_with_retry(f"{BASE_URL}/rate/{currency}/RUB")
    if response.status_code in (404, 422):
        raise NotFoundError(f"валюта {currency} не найдена")

    data = parse_json(response)
    require(data, "rate")
    if not isinstance(data["rate"], (int, float)):
        raise ServiceError("курс пришёл не числом")
    return float(data["rate"])