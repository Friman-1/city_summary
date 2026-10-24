import argparse
import json
import sys

from clients.http import NotFoundError, ServiceError
from processing.service import build_city_summary


def yes_no(flag):
    return "да" if flag else "нет"


def print_summary(summary):
    weather = summary["weather"]
    rates = summary["rates"]
    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']:.1f}°C, {weather['description']}")
    print(f"Тёплая одежда: {yes_no(weather['warm_clothes'])}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']:.2f}")
    print(f"Дорогой курс: {yes_no(rates['expensive'])}")


def main():
    parser = argparse.ArgumentParser(description="Сводка по городу: погода и курс валюты к рублю")
    parser.add_argument("--city", required=True, help="город, например Moscow")
    parser.add_argument("--currency", default="USD", help="код валюты, по умолчанию USD")
    parser.add_argument("--json", action="store_true", help="вывести сводку в формате JSON")
    args = parser.parse_args()

    try:
        summary = build_city_summary(args.city, args.currency.upper())
    except NotFoundError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 3
    except ServiceError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 4

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print_summary(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())