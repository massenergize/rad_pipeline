"""Main module."""
import pandas as pd

DATA_DIR = "../data"
DATA_FILES = {
    "zip_code_community": os.path.join(DATA_DIR, "Zip Code Community.xlsx"),
    "Air-source Heat Pumps": os.path.join(DATA_DIR, "ResidentialASHPProjectDatabase 11.4.2019.xlsx"),
    "Solar Panels": os.path.join(DATA_DIR, "PVinPTSwebsite.xlsx"),
    "Ground-source Heat Pumps": os.path.join(DATA_DIR, "ResidentialandSmallScaleGSHPProjectDatabase.xlsx"),
    "EVs": os.path.join(DATA_DIR, "MOR-EV Stats Page Data Download.xlsx")
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


def load_ashp() -> pd.DataFrame:
    """
    Load raw data from ASHP excel file
    """
    f_ashp = pd.read_excel(data_files["residental_ashp_project_database"], 'Sheet1', skiprows=3)
    df_ashp = f_ashp.drop([0]) #remove first null row for formatting purposes

    return df_ashp


def load_solar() -> pd.DataFrame:
    """
    Load rawa data from PV in PTS excel file
    """
    df_pv = pd.read_excel(data_files["pv_in_pts_website"], 'PV in PTS', skiprows=7)
    return df_pv
