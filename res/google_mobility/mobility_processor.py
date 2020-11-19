'''
Module collects the goolge mobility data
'''
import pandas as pd


DATA = "GIT/group11/res/google_mobility/processed/Global_Mobility_Report (1).csv"

df = pd.read_csv(DATA)

# Get dataframe with countries only
countries_pd = df[df["sub_region_1"].isna()]

del countries_pd["sub_region_1"]
del countries_pd["sub_region_2"]
del countries_pd["iso_3166_2_code"]
del countries_pd["census_fips_code"]

for col in countries_pd.columns:
    print(col)

countries_pd.to_csv("GIT/group11/res/google_mobility/processed/Google_Mobility_Report_countries.csv", index=False)

# 134 countries in file
del countries_pd["country_region_code"]
del countries_pd["country_region"]

global_pd = countries_pd.groupby("date").sum()
global_pd = global_pd.divide(134)

global_pd.to_csv("GIT/group11/res/google_mobility/processed/Google_Mobility_Report_global.csv", index=True)
