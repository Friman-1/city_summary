COLD_TEMP_C = 0
EXPENSIVE_RATE = 100
DEFAULT_DESCRIPTION = "нет данных"


def needs_warm_clothes(temp_c):
    return temp_c < COLD_TEMP_C


def is_expensive(rate):
    return rate > EXPENSIVE_RATE


def description_or_default(description):
    if description:
        return description
    return DEFAULT_DESCRIPTION