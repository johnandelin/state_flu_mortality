# State Influenza & Pneumonia Mortality Dataset

This project curates a dataset combining **public health outcomes** with **socioeconomic indicators** at the U.S. state level. The goal of the project is to explore whether **state-level poverty rates are associated with higher age-adjusted death rates (AADR)** for **influenza and pneumonia**.

The dataset was built by collecting data from **two public APIs**, cleaning the results, and merging them into a single dataset suitable for analysis.

---

# Project Motivation

Influenza and pneumonia remain significant public health concerns in the United States. Socioeconomic factors such as poverty can influence health outcomes by affecting access to healthcare, vaccination rates, and underlying health conditions.

The motivating question for this project is:

> **Do states with higher poverty rates also experience higher age-adjusted death rates from influenza and pneumonia?**

To explore this question, this project combines **CDC mortality data** with **U.S. Census socioeconomic data**.

---

# Data Sources

## CDC – National Center for Health Statistics
Dataset: *Leading Causes of Death: United States*

Provides mortality counts and **age-adjusted death rates (AADR)** by state and year.

API endpoint used:

https://data.cdc.gov/resource/bi63-dtpu.json

More information:

https://data.cdc.gov/National-Center-for-Health-Statistics/NCHS-Leading-Causes-of-Death-United-States/bi63-dtpu/about_data

---

## U.S. Census Bureau – ACS 5-Year Estimates

Provides socioeconomic indicators including:

- population
- median household income
- poverty counts

API documentation:

https://www.census.gov/data/developers/data-sets/acs-5year.html

A free **Census API key** is required to access this data.

---

# Dataset Description

The final dataset contains **state-level observations from 2010–2017** and includes both public health and socioeconomic variables.

### Observations
~416 rows (state-year combinations)

### Variables

| Variable | Description |
|--------|-------------|
| year | Year of observation |
| state | U.S. state |
| cause_of_death | Cause of death (Influenza and pneumonia) |
| population | Total state population |
| median_income | Median household income |
| poverty_count | Number of individuals in poverty |
| poverty_rate | Poverty proportion of population |
| aadr | Age-adjusted death rate per 100,000 |
| deaths | Number of deaths |

