"""Main module."""
import os
import pandas as pd
# from prefect import task, Flow

import rad_pipeline.zipcodes as zc

DATA_DIR = "../data"
SOURCES = ["EVs", "Solar Panels", "Air-source Heat Pumps", "Ground-source Heat Pumps"]

FIELDS = {
    "EVs": {
        "rebate": "Total Amount",
        "zip": "Zip Code",
        "county": "County",
    },
    "Solar Panels": {
        "cost": 'Total Cost with Design Fees',
        "zip": 'Zip',
        "sector": "Facility Type",
        "town": 'City',
        "capacity": "Capacity \n(DC, kW)"
    },
    "Air-source Heat Pumps": {
        "rebate": 'Rebate Amount ', # That's right, with a space at the end...
        "cost": 'Total System Costs',
        "zip": 'Site Zip Code',
        "town": 'Site City/Town',
        "income": 'Receiving an Income-Based Adder?',
    },
    "Ground-source Heat Pumps": {
        "rebate": 'Rebate Amount',
        "cost": 'Total System Cost',
        "zip": 'Site Zip Code',
        "town": 'Site City/Town',
        "income": 'Income-Based Rebate Received?',
    }
}

DATA_FILES = {
    "zip_code_community": os.path.join(DATA_DIR, "raw", "Zip Code Community.xlsx"),
    "Air-source Heat Pumps": os.path.join(DATA_DIR, "raw", "ResidentialASHPProjectDatabase 11.4.2019.xlsx"),
    "Solar Panels": os.path.join(DATA_DIR, "raw", "PVinPTSwebsite.xlsx"),
    "Ground-source Heat Pumps": os.path.join(DATA_DIR, "raw", "ResidentialandSmallScaleGSHPProjectDatabase.xlsx"),
    "EVs": os.path.join(DATA_DIR, "raw", "MOR-EV Stats Page Data Download.xlsx")
}


def data_pull():
    """
    Download raw data files from source to data/raw directory
    """
    print("Not implemented")
    print(data_pull.__doc__)


def data_load(source: str) -> pd.DataFrame:
    """
    Load the raw data from the provided file (excel) into memory
    """
    print("Not implemented")


def data_aggregate(source: str) -> pd.DataFrame:
    """
    Aggregate dataset `source` by municipality and zipcode
    """
    print("Not implemented")


def load_ashp() -> pd.DataFrame:
    """
    Load raw data from ASHP excel file
    """
    f_ashp = pd.read_excel(DATA_FILES["Air-source Heat Pumps"], 'Sheet1', skiprows=3)
    df_ashp = f_ashp.drop([0]) #remove first null row for formatting purposes

    return df_ashp

def data_clean(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Clean raw ASHP program data

    Input:
        - source: One of the sources defined in FIELDS.keys()
        - df: The dataframe loaded from source.  Must contain fields named in the FIELDS dict
    Results:
    - Adds standardized fields:
       - zip_cleaned, zip4_cleaned, zip_valid, zip_exists, town, town_valid
    """

    try:
        field_map = FIELDS[source]
    except KeyError:
        raise ValueError(f"`source not recognized.  Must be one of {FIELDS.keys()}`")

    try:
        clean_zips = zc.clean(df[field_map["zip"]])
        # Join fields
        df_with_zips = pd.concat([clean_zips, df], axis=1)
    except KeyError:
        # Input has no zip field.  Try to simply validate town
        try:
            df_cleaned = zc.validate_town(df, field_map["town"])
            return df_cleaned
        except KeyError:
            raise ValueError("Input has neither zip nor town field.  At least town is required.")


    # Validate town names
    try:
        df_cleaned = zc.validate_zip_town(df_with_zips, field_map["town"], "zip_cleaned")
    except KeyError:
        #No town field provided
        df_with_zips["dummy_town"] = ""
        df_cleaned = zc.validate_zip_town(df_with_zips, "dummy_town", "zip_cleaned")
        df_cleaned.drop("dummy_town", axis=1, inplace=True)
        df_cleaned.town_valid = True


    return df_cleaned


def load_solar() -> pd.DataFrame:
    """
    Load rawa data from PV in PTS excel file
    """
    df_pv = pd.read_excel(DATA_FILES["Solar Panels"], 'PV in PTS', skiprows=7)
    return df_pv


def load_gshp() -> pd.DataFrame:
    """
    Load raw data from GSHP excel file
    """
    df_gshp = pd.read_excel(DATA_FILES["Ground-source Heat Pumps"], 'Sheet1', skiprows=2)
    return df_gshp


def load_evs() -> pd.DataFrame:
    """
    Load raw data from Electric Vehicle excel file
    """
    df_evs = pd.read_excel(DATA_FILES["EVs"], 'Data')
    return df_evs
