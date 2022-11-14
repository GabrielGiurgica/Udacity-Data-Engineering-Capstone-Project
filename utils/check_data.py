"""Provide functions for checking data quality."""

from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def check_data_quality(df: DataFrame, col_id: str, table_name: str) -> None:
    """Check if the table contains data and the id column is not null."""
    assert df.count() > 0, f"Table {table_name} contains no values."

    assert (
        df.where(F.col(col_id).isNull()).count() == 0
    ), f"In table {table_name}, column id {col_id} contains null values."
