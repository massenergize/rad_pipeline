"""
Logic for cleaning and processing zipcode data
"""
import pandas as pd

def clean(zip_series: pd.Series) -> pd.DataFrame:
    """Standardize zipcodes in a pandas series

    Pandas will likely load zipcodes from an excel file as an object series
    mixing string and numeric types.  This function will cast all entries to
    string types, strip whitespace, left pad to a minimum of 5 characters with zeros, then
    validate the entry contains a valid zipcode using a regular expression.

    Return: pandas.DataFrame
    - Pandas series of cleaned zipcodes: str
    - Pandas series of cleaned zip4, or empty string if missing: str
    - Pandas series of valid zipcode indicators: boolean
    """
    # Valid zipcodes are 3-5 numeric digits, followed by an optional dash and 4 more digits, or an optional ".0" if the data has been cast as floats.
    valid_zipcode_regex = r"^([0-9]{3,5})(?:[.]0)?(?:-([0-9]{4})|-)?$"
    #The extract function will match this pattern, and extract the zip5 group into column 0 and the zip4 group into column 1.  NaN if group is not present or pattern isn't matched.
    res = zip_series.astype(str).str.strip().str.extract(valid_zipcode_regex)

    cleaned_zipcode_series = res[0].str.zfill(5).fillna('')
    cleaned_zip4_series = res[1].fillna('')

    valid_zipcode_series = cleaned_zipcode_series.str.match(valid_zipcode_regex)

    #Replace invalid value rows with original inputs
    cleaned_zipcode_series.loc[~valid_zipcode_series] = zip_series[~valid_zipcode_series]
    return pd.DataFrame(data={"zip_cleaned": cleaned_zipcode_series, "zip4_cleaned": cleaned_zip4_series, "zip_valid": valid_zipcode_series})
