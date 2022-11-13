"""Provide functions to read the data."""

import os
from typing import Dict, ItemsView

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


def get_file_path(dir_path: str, file: str) -> str:
    """Join the file name with the directory name and check the path."""
    path = os.path.join(dir_path, file)
    assert os.path.exists(path), f"{path} path doesn't exist!"
    return path


def read_airport_csv(spark: SparkSession, dir_path: str) -> DataFrame:
    """Read airport csv file."""
    csv_path = get_file_path(dir_path, "airport-codes_csv.csv")
    spark_df = spark.read.option("header", True).csv(csv_path)
    print("Airport csv file was successfully read.")
    return spark_df


def read_demographic_csv(spark: SparkSession, dir_path: str) -> DataFrame:
    """Read demographic csv file."""
    csv_path = get_file_path(dir_path, "us-cities-demographics.csv")

    spark_df = spark.read.option("header", True).options(delimiter=";").csv(csv_path)
    print("Demographic csv file was successfully read.")
    return spark_df


def read_immigration_sas(spark: SparkSession) -> DataFrame:
    """Read imiggration SAS files."""
    spark_df = spark.read.format("com.github.saurfang.sas.spark").load(
        "../../data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat"
    )
    print("Immigration SAS files were successfully read.")
    return spark_df


def read_temperature_csv(spark: SparkSession, dir_path: str) -> DataFrame:
    """Read GlobalLandTemperaturesByCity csv file."""
    csv_path = get_file_path(dir_path, "GlobalLandTemperaturesByCity.csv")
    spark_df = spark.read.option("header", True).csv(csv_path)
    print("GlobalLandTemperaturesByCity csv file was successfully read.")
    return spark_df


def read_country_list(spark: SparkSession) -> DataFrame:
    """Read the country list from 'https://countrycode.org/'."""
    link = "https://countrycode.org/"
    pd_df = pd.read_html(link)[1]
    pd_df["ISO CODES"] = pd_df["ISO CODES"].apply(lambda value: value.split(" / ")[0])
    pd_df.drop(columns=["COUNTRY CODE"], inplace=True)
    pd_df.rename(
        columns={"COUNTRY": "country", "ISO CODES": "country_code"}, inplace=True
    )

    spark_df = spark.createDataFrame(pd_df)
    print(f"Country list from {link} was successfully read.")
    return spark_df


def read_us_states_list(spark: SparkSession) -> DataFrame:
    """Read the US states list from 'https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971'."""
    link = "https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971"
    pd_df = pd.read_html(link)[0]
    pd_df.drop(columns=["Abbreviation", "Code"], inplace=True)
    pd_df.rename(columns={"State": "state", "Alpha code": "state_code"}, inplace=True)

    spark_df = spark.createDataFrame(pd_df)
    print(f"US states list from {link} was successfully read.")
    return spark_df


def read_continet_list(spark: SparkSession) -> DataFrame:
    """Read the continent list from 'https://www.php.net/manual/en/function.geoip-continent-code-by-name.php'."""
    link = "https://www.php.net/manual/en/function.geoip-continent-code-by-name.php"
    pd_df = pd.read_html(link, keep_default_na=False)[0]

    spark_df = spark.createDataFrame(pd_df)
    print(f"Continent list from {link} was successfully read.")
    return spark_df


def _extract_value(string: str) -> str:
    """Extract substrings between single quotes."""
    start = string.index("'") + 1
    end = string.index("'", start)
    return string[start:end].strip()


def _remove_symbols(string: str) -> str:
    r"""Remove '\t' and '\n' from the string."""
    return string.replace("\t", "").replace("\n", "").strip()


def _clean_description(data: Dict[str, str]) -> Dict[str, str]:
    """Remove invalid descriptions."""
    invalid_descriptions = ("INVALID", "Collapsed", "No Country", "No PORT")
    return {
        code: descr
        for code, descr in data.items()
        if all(
            [
                inv_descr.lower() not in descr.lower()
                for inv_descr in invalid_descriptions
            ]
        )
    }


def read_i94_descr(
    attribute_name: str, dir_path: str, clean_descr: bool = False
) -> Dict[str, str]:
    """Read the attribute labels from I94_SAS_Labels_Descriptions.SAS."""
    attribute = attribute_name.upper()

    sas_path = get_file_path(dir_path, "I94_SAS_Labels_Descriptions.SAS")
    with open(sas_path) as f:
        lines = f.readlines()

    label_mapping = dict()
    skip_line = True
    for line in lines:
        # Skip the other attributes
        if (attribute not in line) and (skip_line is True):
            continue
        skip_line = False

        # End of attribute description
        if "\n" == line:
            break

        # Skip the attribute explanations
        if "=" not in line:
            continue

        label, descr = line.split("=")
        label = _extract_value(label) if "'" in label else _remove_symbols(label)
        descr = _extract_value(descr) if "'" in descr else _remove_symbols(descr)
        label_mapping.update({label: descr})

    if not label_mapping:
        raise ValueError(
            f"Either {attribute_name} attribute does not exist or has no labels."
        )

    if clean_descr is True:
        label_mapping = _clean_description(label_mapping)

    print(
        "Attribute description {attribute_name} was successfully read from I94_SAS_Labels_Descriptions.SAS."
    )
    return label_mapping


def read_origin_countries(
    dir_path: str,
) -> ItemsView[str, str]:
    """
    Get attribute labels for origin countries from I94_SAS_Labels_Descriptions.SAS.

    Return the codes and description for the i94cit
    and i94res attributes.
    """
    attr_name = "i94res"
    data = read_i94_descr(attr_name, dir_path=dir_path, clean_descr=True)  # OR "i94cit"
    data.update({"582": "MEXICO"})
    print(
        "Attribute description {attr_name} was successfully read from I94_SAS_Labels_Descriptions.SAS."
    )
    return data.items()
