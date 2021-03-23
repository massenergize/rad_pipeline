"""Main module."""
import os
from typing import List

import great_expectations as ge
import numpy as np
import pandas as pd
#from prefect import task, Flow

import rad_pipeline.zipcodes as zc

DATA_DIR = "../data"
SOURCES = ["EVs", "Solar Panels", "Air-source Heat Pumps", "Ground-source Heat Pumps"]

# Mapping of standardized/cleaned field names to raw data field names
# Also communicates which fields are present in each dataset.
FIELDS = {
    "EVs": {
        "rebate": "Total Amount",
        "zip": "Zip Code",
        "county": "County",
        "date": 'Date of Purchase',
    },
    "Solar Panels": {
        "cost": 'Total Cost with Design Fees',
        "zip": 'Zip',
        "sector": "Facility Type",
        "town": 'City',
        "capacity": "Capacity \n(DC, kW)",
        "date": "Date In Service",
    },
    "Air-source Heat Pumps": {
        "rebate": 'Rebate Amount ', # That's right, with a space at the end...
        "cost": 'Total System Costs',
        "zip": 'Site Zip Code',
        "town": 'Site City/Town',
        "income": 'Receiving an Income-Based Adder?',
        "date": 'Date Rebate Payment Approved by MassCEC',
    },
    "Ground-source Heat Pumps": {
        "rebate": 'Rebate Amount',
        "cost": 'Total System Cost',
        "town": 'Site City/Town',
        "income": 'Income-Based Rebate Received?',
        "date": 'Rebate Approved by MassCEC',
    }
}

# Mapping of standardized/cleaned field names to raw field names
# Contains only numeric fields which will be aggregated.
VALUE_FIELDS = {
    "EVs": {
        "rebate": "Total Amount",
    },
    "Solar Panels": {
        "cost": 'Total Cost with Design Fees',
        "capacity": "Capacity \n(DC, kW)"
    },
    "Air-source Heat Pumps": {
        "rebate": 'Rebate Amount ', # That's right, with a space at the end...
        "cost": 'Total System Costs',
    },
    "Ground-source Heat Pumps": {
        "rebate": 'Rebate Amount',
        "cost": 'Total System Cost',
    }
}


RAW_DATA_FILES = {
    "zip_code_community": os.path.join(DATA_DIR, "raw", "Zip Code Community.xlsx"),
    "Air-source Heat Pumps": os.path.join(DATA_DIR, "raw", "ResidentialASHPProjectDatabase 11.4.2019.xlsx"),
    "Solar Panels": os.path.join(DATA_DIR, "raw", "PVinPTSwebsite.xlsx"),
    "Ground-source Heat Pumps": os.path.join(DATA_DIR, "raw", "ResidentialandSmallScaleGSHPProjectDatabase.xlsx"),
    "EVs": os.path.join(DATA_DIR, "raw", "MOR-EV Stats Page Data Download.xlsx")
}


CLEAN_DATA_FILES = {
    "Air-source Heat Pumps": os.path.join(DATA_DIR, "clean", "ashp.{0}.pkl"),
    "Solar Panels": os.path.join(DATA_DIR, "clean", "solar.{0}.pkl"),
    "Ground-source Heat Pumps": os.path.join(DATA_DIR, "clean", "gshp.{0}.pkl"),
    "EVs": os.path.join(DATA_DIR, "clean", "evs.{0}.pkl")
}


EXPECTATION_FILES = {
    "Air-source Heat Pumps": os.path.join(DATA_DIR, "expectations", "ashp_{0}_expectations.json"),
    "Solar Panels": os.path.join(DATA_DIR, "expectations", "solar_{0}_expectations.json"),
    "Ground-source Heat Pumps": os.path.join(DATA_DIR, "expectations", "gshp_{0}_expectations.json"),
    "EVs": os.path.join(DATA_DIR, "expectations", "evs_{0}_expectations.json")
}


SECTOR_LOOKUP = {
    "Air-source Heat Pumps": "Residential",
    "Ground-source Heat Pumps": "Residential and Small Scale",
    "Solar Panels": "All",
    "EVs": "Consumer",
}


def data_pull(source: str):
    """
    Download raw data files from source to data/raw directory
    """
    print("Not implemented")
    print(data_pull.__doc__)


def clean_data_load(source: str) -> pd.DataFrame:
    """
    Load and validate the raw data from the clean data file into memory
    """
    return pd.read_pickle(CLEAN_DATA_FILES[source].format("clean"))


def dq_check(df: pd.DataFrame, source: str, stage: str):
    result = ge.from_pandas(df).validate(EXPECTATION_FILES[source].format(stage))
    print(result)
    assert result.success

    return result


def data_clean(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Clean raw program data

    Input:
        - source: One of the sources defined in FIELDS.keys()
        - df: The dataframe loaded from source.  Must contain fields named in the FIELDS dict
    Results:
    - Adds standardized fields:
       - zip_cleaned, zip4_cleaned, zip_valid, zip_exists, town, town_valid
    - Coerces fields listed in `value_fields` to be numeric. Non-numeric values converted to nans
       - Adds coerced numeric value as field name given in FIELDS map.
    """

    try:
        field_map = FIELDS[source]
    except KeyError:
        raise ValueError(f"`source not recognized.  Must be one of {FIELDS.keys()}`")

    try:
        # Standardize zips into properly formatted strings
        clean_zips = zc.clean(df[field_map["zip"]])
        # Join fields
        df_with_zips = pd.concat([clean_zips, df], axis=1)

        # Validate town names
        try:
            df_cleaned = zc.validate_zip_town(df_with_zips, field_map["town"], "zip_cleaned")
        except KeyError:
            #No town field provided (EVs)
            df_with_zips["dummy_town"] = ""
            df_cleaned = zc.validate_zip_town(df_with_zips, "dummy_town", "zip_cleaned")
            df_cleaned.drop("dummy_town", axis=1, inplace=True)
            df_cleaned.town_valid = True

    except KeyError:
        # Input has no zip field.  Try to simply validate town
        try:
            df_cleaned = zc.validate_town(df, field_map["town"])
        except KeyError:
            raise ValueError("Input has neither zip nor town field.  At least town is required.")

    # Validate numeric value fields
    value_fields = list(VALUE_FIELDS[source].keys())
    for value_field in value_fields:
        df_cleaned[value_field] = pd.to_numeric(df[field_map[value_field]], errors='coerce')

    return df_cleaned


def all_numeric(lst: List) -> bool:
    """
    Checks the values in a list and returns true if all values are numeric without missing values

    NB: string values that can be cast to numeric, e.c. "3.12"
    """
    return not np.isnan(pd.to_numeric(lst, errors='coerce')).any()


def validate_clean_record(row: dict, town_valid_field: str, value_fields: List[str]) -> bool:
    """
    Implement logic for diffrentiating an accepted input record from a rejected input record.

    Currently valid: The town field has been marked valid and all value fields are numeric and present.

    Inputs:
    row: dict  DataFrame row
    town_field: str  Town field name
    value_fields: List[str]  List of numeric value fields being analyzed/aggregated

    Returns:
    Accept/Reject: boolean
    """


    valid = row[town_valid_field] & all_numeric([row[f] for f in value_fields])
    return valid


def data_checkpoint(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Checkpoint cleaned data by splitting into accept and reject files and saving to clean data dir

    Input:
    pandas.DataFrame with cleaned fields: zip_valid, zip_exists, town_valid
    source (Data source): str

    Returns:
    pandas.DataFrame of accepted cleaned records only
    """
    try:
        clean_file = CLEAN_DATA_FILES[source].format("clean")
        reject_file = CLEAN_DATA_FILES[source].format("reject")
    except KeyError:
        raise ValueError(f"Data source '{source}' not recognized.  Must be one of {CLEAN_DATA_FILES.keys()}")

    #Accept records with valid Town identifier.  This implies zip is valid and exists if zip is present.
    #Accept recordes where all value fields are also numeric and non NAN.
    value_fields = list(VALUE_FIELDS[source].values())
    valid_record = df.apply(lambda row: validate_clean_record(row, "town_valid", value_fields), axis=1)
    clean_data = df[valid_record]
    reject_data = df[~valid_record]

    # Use pickle files to retain data types on reload.
    clean_data.to_pickle(clean_file)
    reject_data.to_pickle(reject_file)

    return clean_data


def data_aggregate(df_clean: pd.DataFrame, source: str, locale_key: List[str], value_field: str) -> pd.DataFrame:
    """
    Aggregate a clean dataframe on a locale key (e.g. zipcode, county, county+Sector)
    """


def load_solar() -> pd.DataFrame:
    """
    Load raw data from Photovoltaic (PV) in PTS excel file
    """
    df_pv = pd.read_excel(RAW_DATA_FILES["Solar Panels"], 'PV in PTS', skiprows=7)
    return df_pv


def load_gshp() -> pd.DataFrame:
    """
    Load raw data from GSHP excel file
    """
    df_gshp = pd.read_excel(RAW_DATA_FILES["Ground-source Heat Pumps"], 'Sheet1', skiprows=2)
    return df_gshp


def load_evs() -> pd.DataFrame:
    """
    Load raw data from Electric Vehicle excel file
    """
    df_evs = pd.read_excel(RAW_DATA_FILES["EVs"], 'Data')
    return df_evs


def load_ashp() -> pd.DataFrame:
    """
    Load raw data from ASHP excel file
    """
    f_ashp = pd.read_excel(RAW_DATA_FILES["Air-source Heat Pumps"], 'Sheet1', skiprows=3)
    df_ashp = f_ashp.drop([0]) #remove first null row for formatting purposes

    return df_ashp
