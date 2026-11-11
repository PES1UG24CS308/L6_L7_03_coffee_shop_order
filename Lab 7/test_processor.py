"""Hypothesis fuzz tests and behavior checks for processor.py."""

import pytest
from hypothesis import given, strategies as st

from processor import (
    calculate_average_shot_cost,
    lookup_drink_code,
    parse_order_modifiers,
)


@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        lookup_drink_code(s)
    except Exception as exc:
        assert False, f"lookup_drink_code crashed with {s!r}: {exc}"


@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        calculate_average_shot_cost(s)
    except Exception as exc:
        assert False, f"calculate_average_shot_cost crashed with {s!r}: {exc}"


@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        parse_order_modifiers(s)
    except Exception as exc:
        assert False, f"parse_order_modifiers crashed with {s!r}: {exc}"


@pytest.mark.parametrize(
    ("code", "expected_price"),
    [
        ("LAT", 4.50),
        ("cap", 4.00),
        ("ESPRESSO", 3.00),
        (" AME ", 3.50),
        ("mocha", 5.00),
    ],
)
def test_lookup_drink_code_known_menu_items(code, expected_price):
    assert lookup_drink_code(code) == expected_price


@pytest.mark.parametrize("code", [None, "", "TEA", "  "])
def test_lookup_drink_code_invalid_values_return_none(code):
    assert lookup_drink_code(code) is None


def test_calculate_average_shot_cost_valid_csv():
    assert calculate_average_shot_cost("1.0, 1.5, 2.0") == 1.5


@pytest.mark.parametrize(
    "pricing_csv",
    [
        None,
        "",
        "1.0,,2.0",
        "1.0,not-a-number",
        "NaN,2.0",
        "inf,2.0",
        "1e308,1e308",
    ],
)
def test_calculate_average_shot_cost_invalid_values_return_none(pricing_csv):
    assert calculate_average_shot_cost(pricing_csv) is None


def test_parse_order_modifiers_valid_specification():
    assert parse_order_modifiers("milk:oat;syrup:vanilla") == {
        "milk": "oat",
        "syrup": "vanilla",
    }


def test_parse_order_modifiers_allows_colons_inside_values():
    assert parse_order_modifiers("note:extra:hot") == {"note": "extra:hot"}


def test_parse_order_modifiers_empty_specification_returns_empty_dict():
    assert parse_order_modifiers("") == {}


@pytest.mark.parametrize(
    "order_spec",
    [None, "milk", ":oat", "milk:", "milk:oat;;syrup:vanilla"],
)
def test_parse_order_modifiers_invalid_values_return_none(order_spec):
    assert parse_order_modifiers(order_spec) is None
