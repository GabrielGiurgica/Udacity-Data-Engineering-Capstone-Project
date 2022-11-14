# noqa: D100

import os
from configparser import ConfigParser

import boto3
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType

from utils.check_data import check_data_quality
from utils.config import get_config
from utils.process_data import convert_to_datetime, extract_region
from utils.read_data import (
    get_file_path,
    read_airport_csv,
    read_continet_list,
    read_country_list,
    read_demographic_csv,
    read_i94_descr,
    read_immigration_sas,
    read_origin_countries,
    read_temperature_csv,
    read_us_states_list,
)
from utils.write_data import write_table_data


def create_spark_session() -> SparkSession:
    """Get or create a spark session."""
    spark = (
        SparkSession.builder.config("spark.jars.repositories", "https://repos.spark-packages.org/")
        .config("spark.jars.packages", "saurfang:spark-sas7bdat:2.0.0-s_2.11")
        .enableHiveSupport()
        .getOrCreate()
    )

    return spark


def process_temperature_evolution_foreign_country(
    spark: SparkSession, input_dir_path: str, output_dir_path: str
) -> None:
    """Create/Recreate temperature_evolution_foreign_country dimension table."""
    table_name = "temperature_evolution_foreign_country"

    temp_df = read_temperature_csv(spark, input_dir_path).dropna()

    temp_df = temp_df.withColumn("year", F.year("dt")).withColumn("month", F.month("dt"))
    temp_df = temp_df.groupBy([F.col("Country").alias("country"), "year", "month"]).agg(
        F.avg("AverageTemperature").alias("average_temperature"),
        F.avg("AverageTemperatureUncertainty").alias("average_temperature_uncertainty"),
    )
    temp_df = temp_df.withColumn("temperature_id", F.monotonically_increasing_id())

    check_data_quality(temp_df, "temperature_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(temp_df, output_dir_path, table_name)


def process_demographic(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate demographic dimension table."""
    table_name = "demographic"

    demog_df = read_demographic_csv(spark, input_dir_path)

    demog_df = demog_df.groupBy(F.col("State Code").alias("state_code")).agg(
        F.sum("Total Population").cast(IntegerType()).alias("total_population"),
        F.sum("Male Population").cast(IntegerType()).alias("male_population"),
        F.sum("Female Population").cast(IntegerType()).alias("female_population"),
        F.sum("Number of Veterans").cast(IntegerType()).alias("number_of_veterans"),
        F.sum("Foreign-born").cast(IntegerType()).alias("foregin_born"),
        F.sum("Median Age").cast(FloatType()).alias("median_age"),
        F.sum("Average Household Size").cast(FloatType()).alias("average_household_size"),
    )

    check_data_quality(demog_df, "state_code", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(demog_df, output_dir_path, table_name)


def process_world_airports(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate world_airports dimension table."""
    table_name = "world_airports"

    continent_df = read_continet_list(spark)
    us_states_df = read_us_states_list(spark)
    country_df = read_country_list(spark)
    airport_df = read_airport_csv(spark, input_dir_path)

    airport_df = airport_df.where(F.col("type").isin(["small_airport", "medium_airport", "large_airport"]))
    airport_df = (
        airport_df.join(
            F.broadcast(continent_df),
            F.col("continent") == continent_df.Code,
            how="left",
        )
        .join(
            F.broadcast(country_df),
            F.col("iso_country") == country_df.country_code,
            how="left",
        )
        .join(
            F.broadcast(us_states_df),
            extract_region(F.col("iso_region")) == us_states_df.state_code,
            how="left",
        )
    )

    airport_df = airport_df.select(
        F.col("ident").alias("airport_id"),
        F.col("name").alias("airport_name"),
        F.split(F.col("type"), "_")[0].alias("airport_type"),
        F.col("iata_code"),
        F.col("local_code").alias("municipality_code"),
        F.col("municipality").alias("municipality"),
        extract_region(F.col("iso_region")).alias("region_code"),
        F.col("state").alias("region"),
        F.col("country_code"),
        F.col("country"),
        F.col("Code").alias("continent_code"),
        F.col("Continent name").alias("continent"),
        F.col("elevation_ft").cast(FloatType()),
        F.split(F.col("coordinates"), ", ")[1].cast(FloatType()).alias("latitude"),
        F.split(F.col("coordinates"), ", ")[0].cast(FloatType()).alias("longitude"),
    )

    check_data_quality(airport_df, "airport_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(airport_df, output_dir_path, table_name)


def process_us_states(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate us_states dimension table."""
    table_name = "us_states"

    us_states_df = read_us_states_list(spark)

    check_data_quality(us_states_df, "state_code", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(us_states_df, output_dir_path, table_name)


def process_visa(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate us_states dimension table."""
    table_name = "visa"

    visa_category = read_i94_descr("I94VISA", input_dir_path)
    imm_df = read_immigration_sas(spark)

    dim_visa_df = imm_df.select(
        F.col("visatype").alias("visa_type"),
        F.col("visapost").alias("visa_issuer"),
        F.col("I94VISA").alias("visa_category_code").cast(IntegerType()).cast(StringType()),
    ).dropDuplicates()
    dim_visa_df = dim_visa_df.withColumn("visa_category", F.col("visa_category_code")).replace(
        visa_category, subset="visa_category"
    )

    # Add unique IDs
    window_visa = Window.orderBy("visa_type")
    dim_visa_df = dim_visa_df.withColumn("visa_id", F.row_number().over(window_visa))

    check_data_quality(dim_visa_df, "visa_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(dim_visa_df, output_dir_path, table_name)


def process_applicant_origin_country(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate applicant_origin_country dimension table."""
    table_name = "applicant_origin_country"

    values = read_origin_countries(input_dir_path)

    labels = ["origin_country_code", "origin_country"]
    dim_appl_org_country_df = spark.createDataFrame(values, labels)

    check_data_quality(dim_appl_org_country_df, "origin_country_code", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(dim_appl_org_country_df, output_dir_path, table_name)


def process_status_flag(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate status_flag dimension table."""
    table_name = "status_flag"

    imm_df = read_immigration_sas(spark)

    dim_status_flag = imm_df.select(
        F.col("entdepa").alias("arriaval_flag"),
        F.col("entdepd").alias("departure_flag"),
        F.col("entdepu").alias("update_flag"),
        F.col("matflag").alias("match_flag"),
    ).dropDuplicates()

    # Add unique IDs
    window_arriaval = Window.orderBy("arriaval_flag")
    dim_status_flag_df = dim_status_flag.withColumn("status_flag_id", F.row_number().over(window_arriaval))

    check_data_quality(dim_status_flag_df, "status_flag_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(dim_status_flag_df, output_dir_path, table_name)


def process_admission_port(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate admission_port dimension table."""
    table_name = "admission_port"

    values = read_i94_descr("i94port", input_dir_path, clean_descr=True).items()

    labels = ["admission_port_code", "admission_port"]
    dim_admission_port_df = spark.createDataFrame(values, labels)

    check_data_quality(dim_admission_port_df, "admission_port_code", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(dim_admission_port_df, output_dir_path, table_name)


def process_arriaval_mode(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate arriaval_mode dimension table."""
    table_name = "arriaval_mode"

    mode = read_i94_descr("i94mode", input_dir_path)
    imm_df = read_immigration_sas(spark)

    arriaval_mode_df = imm_df.select(
        F.col("i94mode").alias("mode_code").cast(IntegerType()).cast(StringType()),
        F.col("airline"),
        F.col("fltno").alias("flight_number"),
    ).dropDuplicates()
    arriaval_mode_df = arriaval_mode_df.withColumn("mode", F.col("mode_code")).replace(mode, subset="mode")

    # Add unique IDs
    window_arriaval_mode = Window.orderBy("mode_code")
    arriaval_mode_df = arriaval_mode_df.withColumn("arriaval_mode_id", F.row_number().over(window_arriaval_mode))

    check_data_quality(arriaval_mode_df, "arriaval_mode_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(arriaval_mode_df, output_dir_path, table_name)


def process_date(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate date dimension table."""
    table_name = "date"
    col_id = table_name

    imm_df = read_immigration_sas(spark)

    admission_date_df = imm_df.select(F.to_date(F.col("dtaddto"), "MMddyyyy").alias(col_id)).distinct()
    added_file_date_df = imm_df.select(F.to_date(F.col("dtadfile"), "yyyyMMdd")).distinct()
    arrival_date_df = imm_df.select(convert_to_datetime(F.col("arrdate"))).distinct()
    departure_date_df = imm_df.select(convert_to_datetime(F.col("depdate"))).distinct()
    date_df = (
        admission_date_df.union(admission_date_df)
        .union(added_file_date_df)
        .union(arrival_date_df)
        .union(departure_date_df)
        .distinct()
    )

    date_df = date_df.select(
        F.col(col_id),
        F.year(F.col(col_id)).alias("year"),
        F.quarter(F.col(col_id)).alias("quarter"),
        F.month(F.col(col_id)).alias("month"),
        F.weekofyear(F.col(col_id)).alias("week_of_year"),
        F.dayofweek(F.col(col_id)).alias("day_of_week"),
        F.dayofmonth(F.col(col_id)).alias("day_of_month"),
        F.dayofyear(F.col(col_id)).alias("day_of_year"),
    ).na.drop(subset=[col_id])

    check_data_quality(date_df, col_id, table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(date_df, output_dir_path, table_name)


def process_immigrant_application(spark: SparkSession, input_dir_path: str, output_dir_path: str) -> None:
    """Create/Recreate immigrant_application dimension table."""
    table_name = "immigrant_application"

    imm_df = read_immigration_sas(spark)
    visa_path = get_file_path(output_dir_path, "visa")
    status_flag_path = get_file_path(output_dir_path, "status_flag")
    arriaval_mode_path = get_file_path(output_dir_path, "arriaval_mode")

    visa_df = spark.read.parquet(visa_path)
    status_flag_df = spark.read.parquet(status_flag_path)
    arriaval_mode_df = spark.read.parquet(arriaval_mode_path)

    imm_appl_df = (
        imm_df.join(
            F.broadcast(visa_df),
            (imm_df.visatype == visa_df.visa_type)
            & (imm_df.i94visa == visa_df.visa_category_code)
            & (imm_df.visapost == visa_df.visa_issuer),
            how="left",
        )
        .join(
            F.broadcast(status_flag_df),
            (imm_df.entdepa == status_flag_df.arriaval_flag)
            & (imm_df.entdepd == status_flag_df.departure_flag)
            & (imm_df.entdepu == status_flag_df.update_flag)
            & (imm_df.matflag == status_flag_df.match_flag),
            how="left",
        )
        .join(
            arriaval_mode_df,
            (imm_df.i94mode == arriaval_mode_df.mode_code)
            & (imm_df.airline == arriaval_mode_df.airline)
            & (imm_df.fltno == arriaval_mode_df.flight_number),
            how="left",
        )
    )
    imm_appl_df = imm_appl_df.select(
        F.col("cicid").alias("file_id").cast(IntegerType()),
        F.col("insnum").alias("ins_number").cast(IntegerType()),
        F.col("admnum").alias("admission_number").cast(IntegerType()),
        F.col("i94bir").alias("applicant_age"),
        F.col("biryear").alias("applicant_birth_year"),
        F.col("gender"),
        F.col("occup").alias("occupation"),
        F.col("visa_id"),
        F.to_date(F.col("dtadfile"), "yyyyMMdd").alias("application_date"),
        F.col("i94port").alias("admission_port_code"),
        F.col("i94addr").alias("arriaval_state_code"),
        F.col("arriaval_mode_id"),
        convert_to_datetime(F.col("arrdate")).alias("arriaval_date"),
        convert_to_datetime(F.col("depdate")).alias("departure_date"),
        F.to_date(F.col("dtaddto"), "MMddyyyy").alias("limit_date"),
        F.col("status_flag_id"),
        F.col("i94cit").alias("birth_country"),
        F.col("i94res").alias("residence_country"),
    )

    check_data_quality(imm_appl_df, "file_id", table_name)
    print(f"Data for {table_name} table was successfully processed.")

    write_table_data(imm_appl_df, output_dir_path, table_name)


def upload_to_s3(config: ConfigParser, data_path: str) -> None:
    """
    Upload the processed data to S3.

    This function is taken over and slightly modified from:
    https://www.developerfiles.com/upload-files-to-s3-with-python-keeping-the-original-folder-structure/
    """
    key = config["AWS"]["KEY"]
    secret = config["AWS"]["SECRET"]
    s3_bucket = config["AWS"]["S3"]

    session = boto3.Session(aws_access_key_id=key, aws_secret_access_key=secret, region_name="us-east-1")
    s3 = session.resource("s3")
    bucket = s3.Bucket(s3_bucket)

    for subdir, dirs, files in os.walk(data_path):
        if not files:
            continue
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, "rb") as data:
                bucket.put_object(Key=full_path[len(data_path) + 1 :], Body=data)
        print(f"{subdir} table was succesfully loaded into {s3_bucket}.")
    print(f"\nAll the tables were succesfully loaded into {s3_bucket}.")


def main():
    # noqa: D103

    spark = create_spark_session()

    input_data = "raw_data"
    output_data = "processed_data"
    config = get_config("df.cfg")

    process_tables = (
        process_temperature_evolution_foreign_country,
        process_demographic,
        process_world_airports,
        process_us_states,
        process_visa,
        process_applicant_origin_country,
        process_status_flag,
        process_admission_port,
        process_arriaval_mode,
        process_date,
        process_status_flag,
        process_immigrant_application,
    )
    for process_tab in process_tables:
        process_tab(spark, input_data, output_data)
        print("")

    upload_to_s3(config, data_path=output_data)


if __name__ == "__main__":
    main()
