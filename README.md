# Udacity Data Engineering Capstone Project

_________________

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
_________________

## Contents

1. [Project Summary](#project-summary)  
2. [Data Sources](#data-sources)  
3. [Data Model](#data-model)   
4. [ETL Pipeline](#etl-pipeline)
5. [Other Scenarios](#other-scenarios)
6. [Structure of the project](#structure-of-the-project)

## Project Summary

This project aims to create an ETL pipeline that takes data from 7 sources, processes them and uploads them to Amazon S3 to be analyzed later. The resulting data are used as a data source for a Data Warehouse whose purpose is to analyze the immigration phenomenon in the US.

This repository is the result of completing the [Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027) on Udacity. So the code was tested in Project Workspace on Udacity.

## Data Sources

As mentioned in the previous section, 7 data sources are used in this project. 4 of them are suggested by Udacity Provided Project and 3 of them are taken from various web pages. A small description of each of them can be found below:
- [I94 Immigration Data](https://www.trade.gov/national-travel-and-tourism-office): 
- [World Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data): This dataset came from Kaggle. It provides historical information about monthly average temperatures in different cities around the world.
- [U.S. City Demographic Data](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/): This dataset contains information on the demographics of all US cities with a population greater than 63 000.
- [Airport Code Table](https://datahub.io/core/airport-codes#data): Provides information about airports around the world.
- [Country Codes](https://countrycode.org/): This site provides the name and 2-letter code of all countries in the world.
- [US States Codes](https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971):  This site provides the name and 2-letter code of all US states.
- [Continent codes](https://www.php.net/manual/en/function.geoip-continent-code-by-name.php): This site provides the name and 2-letter code of all continents.

## Data Model

## ETL Pipeline

## Other Scenarios

### The data was increased by 100x.

### The data populates a dashboard that must be updated on a daily basis by 7am every day.

### The database needed to be accessed by 100+ people.

## Structure of the project