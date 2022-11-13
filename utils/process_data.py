"""Provide functions to process pyspark.sql.DataFrames columns."""

import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, StringType


@F.udf(returnType=StringType())
def extract_region(iso_region: F.col) -> StringType:
    """
    Extract region from iso_region.

    This function is designed to work with airport CSV file data.
    """
    if iso_region is not None:
        return "-".join(iso_region.split("-")[1:])


@F.udf(returnType=DateType())
def convert_to_datetime(date: F.col) -> StringType:
    """Convert timestamp to yyyy-mm-dd format."""
    if date is not None:
        return pd.Timestamp("1960-1-1") + pd.to_timedelta(date, unit="D")
