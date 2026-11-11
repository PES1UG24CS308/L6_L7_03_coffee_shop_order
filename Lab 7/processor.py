"""Coffee shop input-processing helpers used in the Lab 7 fuzzing exercise."""

import math


MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,
}


def lookup_drink_code(code_string):
    """Return the price for a drink code, or None for invalid input."""
    if not isinstance(code_string, str):
        return None

    code_prefix = code_string.strip().upper()[:3]
    return MENU_PRICES.get(code_prefix)


def calculate_average_shot_cost(pricing_csv):
    """Return the average of comma-separated prices, or None if invalid."""
    if not isinstance(pricing_csv, str):
        return None

    entries = pricing_csv.split(",")
    if not entries or any(not entry.strip() for entry in entries):
        return None

    try:
        prices = [float(entry.strip()) for entry in entries]
    except ValueError:
        return None

    if any(not math.isfinite(price) for price in prices):
        return None

    average = sum(prices) / len(prices)
    return average if math.isfinite(average) else None


def parse_order_modifiers(order_spec):
    """Parse semicolon-separated key:value pairs, or return None if invalid."""
    if not isinstance(order_spec, str):
        return None

    if not order_spec.strip():
        return {}

    modifier_dict = {}
    for item in order_spec.split(";"):
        item = item.strip()
        if not item:
            return None

        key, separator, value = item.partition(":")
        key = key.strip()
        value = value.strip()
        if not separator or not key or not value:
            return None

        modifier_dict[key] = value

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
