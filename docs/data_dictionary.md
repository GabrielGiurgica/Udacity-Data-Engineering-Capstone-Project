# Data Dictionary

## immigran_application Table

It is the fact table in the data model. It has as a data source both the I94 Immigration Data dataset and the visa, status_flag and arrival_mode tables from which it takes the id columns. This table contains information about applications submitted by immigrants.

| Column               | Descritpion                                                                                        |
|----------------------|----------------------------------------------------------------------------------------------------|
| file_id              | The unique number of the file.                                                                     |
| ins_number           | INS number                                                                                         |
| admission_number     | Admission Number                                                                                   |
| applicant_age        | Age of the applicant                                                                               |
| applicant_birth_year | The applicant's year of birth                                                                      |
| gender               | Gender of the applicant                                                                            |
| occupation           | A 3-character code indicating the occupation the applicant will have in the U.S.                   |
| visa_id              | The ID that indicates the visa information in the visa table.                                      |
| application_date     | The date the application was added to the I94 files.                                               |
| admission_port_code  | Port of admission                                                                                  |
| arrival_state_code  | The US state where the applicant arrived.                                                          |
| arrival_mode_id     | The ID indicating information about how the applicant arrived in the US in the arrival_mode table. |
| arrival_date        | Date of applicant's arrival to the US.                                                             |
| departure_date       | Date of applicant's departure to the US.                                                           |
| limit_date           | The deadline until which the applicant has the right to stay in the USA.                           |
| status_flag_id       | The ID indicating information about the status of various flags in the status_flag table.          |
| birth_country        | 3-digit code indicating the applicant's country of birth.                                          |
| residence_country    | 3-digit code indicating the applicant's country of residence.                                      |

## visa Table

It is a table of dimensions whose data source is the I94 Immigration Data dataset and its description file. It contains all valid visa information.

| Column             | Descritpion                                                                        |
|--------------------|------------------------------------------------------------------------------------|
| visa_id            | A unique ID                                                                        |
| visa_type          | Class of admission legally admitting the non-immigrant to temporarily stay in U.S. |
| visa_issuer        | Department of State where where Visa was issued.                                   |
| visa_category_code | Visa codes collapsed into three categories.                                        |
| visa_category      | Description of the three visa categories.                                          |

## admission_port Table

It is a dimension table whose data source is the description file in the I94 Immigration Data dataset. It contains the code and information about the admission port through which the immigrant passed.

| Column              | Descritpion                                                                         |
|---------------------|-------------------------------------------------------------------------------------|
| admission_port_code | A 3-letter code indicating the port of admission.                                   |
| admission_port      | A description of the admission port code indicating information about its location. |

## us_states Table

It is a dimension table whose data source is the US States Codes dataset. It contains the name and 2-letter code of all US states.

| Column     | Descritpion                                   |
|------------|-----------------------------------------------|
| state_code | A 2-letter code indicating the US state name. |
| state      | US state name                                 |

## world_airports Table

It is a dimension table whose data sources are the Airport Code Table and Continent Codes datasets. It contains data about all airports in the world.

| Column            | Descritpion                                                                                                                          |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| airport_id        | A code consisting of 3 to 7 characters representing the airport identification code.                                                 |
| airport_name      | Airport name.                                                                                                                        |
| airport_type      | Indicates the size of the airport (small, medium or large).                                                                          |
| iata_code         | It is a geocode designating many airports and metropolitan areas around the world.                                                   |
| municipality_code | A code consisting of 1 to 7 characters representing the identification code of the municipality in which the airport is located.     |
| municipality      | The name of the municipality where the airport is located.                                                                           |
| region_code       | A code consisting of 1 to 4 characters representing the identification code of the region of a country where the airport is located. |
| region            | The name of the region in a country where the airport is located.                                                                    |
| country_code      | A 2-character code representing the identification code of the country where the airport is located.                                 |
| country           | The name of the country where the airport is located.                                                                                |
| continent_code    | A 2-character code representing the identification code of the continent where the airport is located.                               |
| continent         | The name of the continet where the airport is located.                                                                               |
| elevation_ft      | The altitude in feet at which the airport is located.                                                                                |
| latitude          | The latitude of the GPS coordinates.                                                                                                 |
| longitude         | The longitude of the GPS coordinates.                                                                                                |

## country_temperature_evolution Table

It is a dimension table whose data source is the World Temperature Data dataset. It stores the average monthly temperatures of each country from 1743 to 2013.

| Column                          | Descritpion                                                |
|---------------------------------|------------------------------------------------------------|
| temperature_id                  | A unique ID                                                |
| country                         | The name of the country where the measurements were taken. |
| year                            | The year in which the measurements were made.              |
| month                           | The month in which the measurements were made.             |
| average_temperature             | Average temperature during the recorded month.             |
| average_temperature_uncertainty | Average temperature uncertainty during the recorded month. |

## applicant_origin_country Table

It is a dimension table whose data source is the description file in the I94 Immigration Data dataset. It contains a 3-digit code and the name of each country from which an immigrant could come.

| Column              | Descritpion                                                  |
|---------------------|--------------------------------------------------------------|
| origin_country_code | A 3-digit code indicating the applicant's country of origin. |
| origin_country      | The name of the applicant's country of origin.               |

## status_flag Table

It is a dimension table whose data source the I94 Immigration Data dataset. It contains the one-letter status for different stages that the immigrant went through.

| Column         | Descritpion                                |
|----------------|--------------------------------------------|
| arrival_flag  | 1 character indicating the arrival flag.   |
| departure_flag | 1 character indicating the departure flag. |
| update_flag    | 1 character indicating the update flag.    |
| match_flag     | 1 character indicating the match flag.     |
|                |                                            |

## date Table

It is a dimension table whose data source the I94 Immigration Data dataset. It contains all possible data from the columns in the source dataset.

| Column       | Descritpion                           |
|--------------|---------------------------------------|
| date         | The date is in the format YYYY-MM-DD. |
| year         |                                       |
| quarter      | Quarter number of the year.           |
| month        | Month number of the year.             |
| week_of_year | Week number of the year.              |
| day_of_week  | Day number of the week.               |
| day_of_month | Day number of the month.              |
| day_of_year  | Day number of the year.               |

## arrival_mode Table

It is a table of dimensions whose data source is the I94 Immigration Data dataset and its description file. It contains information about how the immigrant arrived in the US.

| Column           | Descritpion                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| arrival_mode_id  | A unique ID                                                                                   |
| mode_code        | A code indicating the mode of transport.                                                      |
| mode             | Description of the code indicating the mode of transport.                                     |
| airline          | A code consisting of 1 to 3 characters representing the airline code used to arrive in U.S.   |
| flight_number    | A 1- to 5-character code that represents the airline flight number used to arrive in the U.S. |

## demographic Table

It is a dimension table whose data source is the U.S. City Demographic Data dataset. It contains population data for each US state.

| Column                 | Descritpion                                   |
|------------------------|-----------------------------------------------|
| state_code             | A 2-letter code indicating the US state name. |
| total_population       | Total population of the state.                |
| male_population        | Total male population of the state.           |
| female_population      | Total female population of the state.         |
| number_of_veterans     | Total number of state veterans.               |
| foregin_born           | Total number of foreign born.                 |
| median_age             | The average age of the state's population.    |
| average_household_size | Average household size in the state.          |
