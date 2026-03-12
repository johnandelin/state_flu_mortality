import requests
import pandas as pd
import time

# --------------------------------
# Load Census API key
# --------------------------------
API = pd.read_csv("API_Keys.csv")
API_CENSUS = API.iloc[1,1]  # adjust index if needed

# --------------------------------
# Parameters
# --------------------------------
years = list(range(2010, 2018))  # 2010–2017

# --------------------------------
# Collect Census Data
# --------------------------------
print("Collecting Census data...")

census_vars = ["B01003_001E","B19013_001E","B17001_002E"]  # population, median_income, poverty_count
census_data = []

for year in years:
    url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=NAME,{','.join(census_vars)}"
        f"&for=state:*"
        f"&key={API_CENSUS}"
    )

    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        header = json_data[0]

        for row in json_data[1:]:
            row_dict = dict(zip(header, row))
            row_dict["year"] = year
            census_data.append(row_dict)
    else:
        print(f"Census error {response.status_code} for {year}")

    time.sleep(0.5)  # gentle pause for API

census_df = pd.DataFrame(census_data)

# Rename columns
census_df.rename(
    columns={
        "B01003_001E": "population",
        "B19013_001E": "median_income",
        "B17001_002E": "poverty_count",
        "NAME": "state_name",
        "state": "state_code"
    },
    inplace=True
)

# Convert numeric
census_df["population"] = pd.to_numeric(census_df["population"])
census_df["median_income"] = pd.to_numeric(census_df["median_income"])
census_df["poverty_count"] = pd.to_numeric(census_df["poverty_count"])

print("Census rows:", census_df.shape[0])

# --------------------------------
# Collect NCHS Influenza & Pneumonia Deaths via SODA2 JSON
# --------------------------------
print("Collecting NCHS influenza & pneumonia deaths...")

base_url = "https://data.cdc.gov/resource/bi63-dtpu.json"
all_data = []
limit = 50000
offset = 0

while True:
    params = {
        "$limit": limit,
        "$offset": offset,
        "$where": "cause_name='Influenza and pneumonia'"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        break
    
    batch = response.json()
    if not batch:
        break
    
    all_data.extend(batch)
    offset += limit
    print(f"Fetched {len(all_data)} rows so far...")
    time.sleep(0.2)

cdc_df = pd.DataFrame(all_data)

if not cdc_df.empty:
    cdc_df["year"] = pd.to_numeric(cdc_df["year"], errors="coerce")
    cdc_df["deaths"] = pd.to_numeric(cdc_df["deaths"], errors="coerce")
    cdc_df["aadr"] = pd.to_numeric(cdc_df["aadr"], errors="coerce")
    print("CDC influenza & pneumonia data loaded:", cdc_df.shape[0])
else:
    print("No influenza & pneumonia deaths data loaded")

# --------------------------------
# Merge Datasets
# --------------------------------
print("Merging datasets...")

final_df = pd.merge(
    census_df,
    cdc_df,
    left_on=["state_name","year"],
    right_on=["state","year"],
    how="left"
)

# Feature engineering

final_df["poverty_rate"] = final_df["poverty_count"] / final_df["population"]
final_df["cause_of_death"] = final_df["cause_name"]
final_df = final_df[["year", "state", "cause_of_death", "population", "median_income", "poverty_count", "aadr", "poverty_rate"]]

print(final_df.isna().sum())# CDC might not have reported 

# Save dataset
final_df.to_csv("influenza_pneumonia_dataset.csv", index=False)

print("Dataset saved! Shape:", final_df.shape)
print(final_df.head())