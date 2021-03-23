import os
import re

import great_expectations as ge
import numpy as np
import pandas as pd

from typing import Tuple

import rad_pipeline.rad_pipeline as rp
import rad_pipeline.zipcodes as zc

def locale_aggregation(df_cleaned: pd.DataFrame, locale_field: str, source: str) -> Tuple[pd.core.groupby.generic.DataFrameGroupBy, pd.DataFrame]:
    field_map = rp.FIELDS[source]
    groups = df_cleaned.groupby(locale_field)
    zipcodes = groups['zip_cleaned'].\
                    apply(lambda x: list(np.unique(x))).\
                    rename_axis("locale")
    start_date = groups[field_map['date']].\
                min().\
                rename_axis("locale").rename("start_date")
    end_date = groups[field_map['date']].\
                    max().\
                    rename_axis("locale").rename("end_date")

    result = pd.DataFrame(data = {
        "zipcodes": zipcodes,
        "start_date": start_date,
        "end_date": end_date,
    })

    return groups, result


def locale_sector_aggregation(df_cleaned: pd.DataFrame, locale_field: str, source: str) -> Tuple[pd.core.groupby.generic.DataFrameGroupBy, pd.DataFrame]:
    field_map = rp.FIELDS[source]
    sector_field = field_map["sector"]
    groups = df_cleaned.groupby([locale_field, sector_field])
    zipcodes = groups['zip_cleaned'].\
                    apply(lambda x: list(np.unique(x))).\
                    rename_axis(["locale", "sector"])
    start_date = groups[field_map['date']].\
                    min().\
                    rename_axis(["locale", "sector"]).rename("start_date")
    end_date = groups[field_map['date']].\
                    max().\
                    rename_axis(["locale", "sector"]).rename("end_date")

    result = pd.DataFrame(data = {
        "zipcodes": zipcodes,
        "start_date": start_date,
        "end_date": end_date,
    })

    return groups, result


EXPECTATION_FILE = os.path.join(rp.DATA_DIR, "expectations", "summarized_expectations.json")


def output_dq_check(df: pd.DataFrame):
    result = ge.from_pandas(df).validate(EXPECTATION_FILE)
    print(result)
    assert result.success
    return result


def save_summarized_metrics(df: pd.DataFrame):
    df.to_parquet(os.path.join(rp.DATA_DIR, "output", "RAD_metrics.parquet"))
    df.to_excel(os.path.join(rp.DATA_DIR, "output", "RAD_metrics.xlsx"))


def compute_summarized_metrics() -> pd.DataFrame():

    metric_groups = []
    for source in ["Air-source Heat Pumps", "Ground-source Heat Pumps", "EVs", "Solar Panels"]:
        try:
            df_cleaned = rp.clean_data_load(source)
            print(f"Loaded {source}")
        except FileNotFoundError:
            print(f"Skipping {source}")
            continue

        for locale_field in ["town", "zip_cleaned"]:


            groups, locale_base = locale_aggregation(df_cleaned, locale_field, source)

            base_df = locale_base.copy()
            base_df["technology"] = source
            base_df["sector"] = rp.SECTOR_LOOKUP[source]

            if "rebate" in df_cleaned.columns:
                # Quantity of Rebates
                metric_group = base_df.copy()
                metric_group["value_unit"] = "count"
                metric_group["metric_name"] = "Number of Rebates"
                metric_group["value"] = groups['rebate'].count()
                metric_groups.append(metric_group)

                # Dollar Total of Rebates
                metric_group = base_df.copy()
                metric_group["value_unit"] = "$USD"
                metric_group["metric_name"] = "Total Rebate Value"
                metric_group["value"] = groups['rebate'].sum()
                metric_groups.append(metric_group)

                # Dollar Average of Rebates
                metric_group = base_df.copy()
                metric_group["value_unit"] = "$USD"
                metric_group["metric_name"] = "Average Rebate Value"
                metric_group["value"] = groups['rebate'].mean()
                metric_groups.append(metric_group)

            if "cost" in df_cleaned.columns:
                # Dollar Total of Costs
                metric_group = base_df.copy()
                metric_group["value_unit"] = "$USD"
                metric_group["metric_name"] = "Total Cost"
                metric_group["value"] = groups['cost'].sum()
                metric_groups.append(metric_group)

                # Dollar Average of Costs
                metric_group = base_df.copy()
                metric_group["value_unit"] = "$USD"
                metric_group["metric_name"] = "Average Cost"
                metric_group["value"] = groups['cost'].mean()
                metric_groups.append(metric_group)

            if "capacity" in df_cleaned.columns: # Solar only

                # Quantity of Solar Panel facilitys
                metric_group = base_df.copy()
                metric_group["value_unit"] = "count"
                metric_group["metric_name"] = "Number of generation facilities"
                metric_group["value"] = groups['capacity'].count()
                metric_groups.append(metric_group)

                # Total Panel Power Capacity
                metric_group = base_df.copy()
                metric_group["value_unit"] = "kW"
                metric_group["metric_name"] = "Total Generation Capacity"
                metric_group["value"] = groups['capacity'].sum()
                metric_groups.append(metric_group)

                # Average Power Capacity
                metric_group = base_df.copy()
                metric_group["value_unit"] = "kW"
                metric_group["metric_name"] = "Average Generation Capacity"
                metric_group["value"] = groups['capacity'].mean()
                metric_groups.append(metric_group)

    RAD_df1 = pd.concat(metric_groups, axis=0)

    # Sector-level aggregation for Solar Panels
    metric_groups = []
    df_cleaned = rp.clean_data_load("Solar Panels")
    for locale_field in ["town", "zip_cleaned"]:
        groups, locale_base = locale_sector_aggregation(df_cleaned, locale_field, "Solar Panels")

        base_df = locale_base.copy()
        base_df["technology"] = source

        if "capacity" in df_cleaned.columns: # Solar only

            # Quantity of Solar Panel facilitys
            metric_group = base_df.copy()
            metric_group["value_unit"] = "count"
            metric_group["metric_name"] = "Number of generation facilities"
            metric_group["value"] = groups['capacity'].count()
            metric_groups.append(metric_group)

            # Total Panel Power Capacity
            metric_group = base_df.copy()
            metric_group["value_unit"] = "kW"
            metric_group["metric_name"] = "Total Generation Capacity"
            metric_group["value"] = groups['capacity'].sum()
            metric_groups.append(metric_group)

            # Average Power Capacity
            metric_group = base_df.copy()
            metric_group["value_unit"] = "kW"
            metric_group["metric_name"] = "Average Generation Capacity"
            metric_group["value"] = groups['capacity'].mean()
            metric_groups.append(metric_group)

    RAD_df2 = pd.concat(metric_groups, axis=0).reset_index("sector")

    return pd.concat([RAD_df1, RAD_df2], axis=0)
