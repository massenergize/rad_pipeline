#!/usr/bin/env python

"""Tests for `rad_pipeline` package."""

import pandas as pd
import pytest

from rad_pipeline import rad_pipeline
from rad_pipeline import zipcodes


@pytest.fixture
def pathalogical_test_cases():
    pathalogical_test_case = pd.Series(data = [2186.0, "2186", 2186, "01545-", "   1590 ", "01545-2790", "12345-123", "02128y", 176.2])
    correct_output = pd.DataFrame(data={
        "zip_cleaned": ["02186", "02186", "02186", "01545", "01590", "01545", "12345-123", "02128y", 176.2],
        "zip4_cleaned": ["", "", "", "", "", "2790", "", "", ""],
        "zip_valid": [True, True, True, True, True, True, False, False, False]
    })
    return {"input": pathalogical_test_case, "expected": correct_output}


def test_zipcleaning(pathalogical_test_cases):
    """Test that zip cleaning works correctly on pathalogical inputs"""
    z_df = zipcodes.clean(pathalogical_test_cases["input"])
    pd.testing.assert_frame_equal(z_df, pathalogical_test_cases["expected"])


def test_validate_zip_town_row():
    #TODO
    assert 0 == 1


def test_all_numeric(): #lst: List -> bool:
    """
    Checks the values in a list and returns true if all values are numeric without missing values

    NB: string values that can be cast to numeric, e.c. "3.12"
    """
    assert rad_pipeline.all_numeric([1,2.54,3])
    assert rad_pipeline.all_numeric([1, "3", 47.2])
    assert not rad_pipeline.all_numeric([1, "Howdy DOody", 25])
