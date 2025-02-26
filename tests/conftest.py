"""Fixtures."""

import os
import json
import pytest

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENCODING = "utf-8"

EGN = "0011223344"
LICENSE = "123456789"

INVALID_EGN = "9988776655"
INVALID_LICENSE = "123"


def load_json(local_path: str):
    """Base method for loading json."""
    path = os.path.join(_BASE_DIR, local_path)

    with open(path, encoding="utf-8") as fixture:
        return json.load(fixture)


@pytest.fixture(name="ok_no_fines")
def ok_no_fines():
    """No obligations JSON."""

    return load_json("fixtures/ok_no_fines.json")


@pytest.fixture(name="ok_fine_sample")
def ok_fine_sample():
    """No obligations JSON."""

    return load_json("fixtures/ok_fine_sample.json")


@pytest.fixture(name="ok_fine_served")
def ok_fine_served():
    """No obligations JSON."""

    return load_json("fixtures/ok_fine_served.json")


@pytest.fixture(name="ok_fine_not_served")
def ok_fine_not_served():
    """No obligations JSON."""

    return load_json("fixtures/ok_fine_not_served.json")


@pytest.fixture(name="err_apidown")
def err_apidown():
    """No obligations JSON."""

    return load_json("fixtures/err_apidown.json")


@pytest.fixture(name="err_nodatafound")
def err_nodatafound():
    """No obligations JSON."""

    return load_json("fixtures/err_nodatafound.json")


@pytest.fixture(name="ok_sample1_2fines")
def ok_sample1_2fines():
    """No obligations JSON."""

    return load_json("fixtures/ok_sample1_2fines.json")


@pytest.fixture(name="ok_sample2_6fines")
def ok_sample2_6fines():
    """No obligations JSON."""

    return load_json("fixtures/ok_sample2_6fines.json")


@pytest.fixture(name="ok_sample3_2fines")
def ok_sample3_2fines():
    """No obligations JSON."""

    return load_json("fixtures/ok_sample3_2fines.json")


@pytest.fixture(name="ok_sample4_1fine")
def ok_sample4_1fine():
    """No obligations JSON."""

    return load_json("fixtures/ok_sample4_1fine.json")
