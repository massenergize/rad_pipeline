"""
Logic for cleaning and processing zipcode data
"""
import pandas as pd
import zipcodes

def clean(zip_series: pd.Series) -> pd.DataFrame:
    """Standardize zipcode formatting in a pandas series

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


def validate_zip_town_row(row: dict, town_field: str, zip_field: str) -> pd.Series:
    """
    Use zipcodes library to append town data from zipcodes and validate existing zip/town inputs
    """
    INVALID_RESULT = {
        "town": "INVALID",
        "zip_exists": False,
        "town_valid": False,
    }
    try:
        zip_results = zipcodes.matching(row[zip_field])
    except TypeError:
        return pd.Series(INVALID_RESULT)
    except ValueError:
        return pd.Series(INVALID_RESULT)
        
    if len(zip_results) > 1:
        raise ValueError(f"Multimatch zipcode {row[zip_field]} encountered!")
    elif len(zip_results) == 0:
        output = INVALID_RESULT
    else: # len(zip_results)==1

        zip_results = zip_results[0]
        standardized_raw_town_name = str(row[town_field]).lower().strip()
        standardized_town_name = zip_results["city"].lower().strip()
        standardized_acceptable_towns = [x.lower().strip() for x in zip_results["acceptable_cities"]]
        standardized_acceptable_towns.append(standardized_town_name)

        #Strict exact matching for now
        town_valid = standardized_raw_town_name in standardized_acceptable_towns
        output = {
            "town": zip_results["city"],
            "zip_exists": True,
            "town_valid": town_valid
        }
    return pd.Series(output)


def validate_zip_town(df: pd.DataFrame, town_field: str, zip_field: str) -> pd.DataFrame:
    """
    Use zipcodes library to append town data from zipcodes and validate existing zip/town inputs

    Return: pandas.DataFrame
    - Pandas series of town name from zipcodes library: str
    - Pandas series indicating zipcode exists: boolean
    - Pandas series indicating raw data town is valid given zipcode: boolean
    """
    return df.merge(df.apply(lambda row: validate_zip_town_row(row, town_field, zip_field), axis=1), left_index=True, right_index=True)
