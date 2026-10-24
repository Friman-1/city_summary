import logging
import time

import requests

logger = logging.getLogger(__name__)

TIMEOUT = (3, 7)
RETRIES = 2
RETRY_CODES = (500, 502, 503, 504)


class NotFoundError(Exception):
    pass


class ServiceError(Exception):
    pass


def get_with_retry(url, params=None):
    for attempt in range(RETRIES + 1):
        wait = 2 ** attempt
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "")
                if retry_after.isdigit():
                    wait = int(retry_after)
            elif response.status_code not in RETRY_CODES:
                return response
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            pass

        if attempt < RETRIES:
            logger.warning("повтор %d из %d через %d с: %s", attempt + 1, RETRIES, wait, url)
            time.sleep(wait)

    raise ServiceError(f"сервис не отвечает после {RETRIES + 1} попыток: {url}")


def parse_json(response):
    if response.status_code != 200:
        raise ServiceError(f"сервис ответил кодом {response.status_code}")
    try:
        data = response.json()
    except ValueError:
        raise ServiceError("сервис вернул не JSON")
    if not isinstance(data, dict):
        raise ServiceError("в ответе ожидался JSON-объект")
    return data


def require(data, *fields):
    if not isinstance(data, dict):
        raise ServiceError("в ответе ожидался JSON-объект")
    missing = [field for field in fields if field not in data]
    if missing:
        raise ServiceError(f"в ответе не хватает полей: {', '.join(missing)}")
    for field in fields:
        if field not in data:
            raise ServiceError(f"в ответе нет поля {field}")