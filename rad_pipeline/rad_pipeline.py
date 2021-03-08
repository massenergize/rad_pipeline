"""Main module."""
import os
import pandas as pd

DATA_DIR = "../data"
SOURCES = ["EVs", "Solar Panels", "Air-source Heat Pumps", "Ground-source Heat Pumps"]

FIELDS = {
    "EVs": {
        "rebate": "Total Amount",
        "zip": "Zip Code",
    },
    "Solar Panels": {
        "rebate": '',
        "cost": '',
        "zip": '',
        "town": '',
        "income": '',
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
    print("Not implemented")


def data_load(source: str) -> pd.DataFrame:
    """
    Load the raw data from the provided file (excel)
    """
    print("Not implemented")


def data_clean(source: str) -> pd.DataFrame:
    """
    Apply data cleaning rules for source
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
