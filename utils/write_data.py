"""Provide functions to write the data."""

import os

from pyspark.sql.dataframe import DataFrame


def write_table_data(df: DataFrame, output_dir_path: str, table_name: str) -> None:
    """Write the data for the table in parquet format."""
    os.makedirs(output_dir_path, exist_ok=True)
    output_path = os.path.join(output_dir_path, table_name)
    df.write.mode("overwrite").parquet(output_path)
    print(f"Data for {table_name} table is saved in {output_path}.")
