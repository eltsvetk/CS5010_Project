#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Jonathan Shakes (hqe7rd@)
CS5010 
Exercise: Data Cleaning
April 3, 2021

Part of Team 4 (Climate Change) Project Work

A data-cleaning Challenge for my team's project: 
stitch together county-level data from 4 separate data sources:
    Census Population data
    Land-area data in each county (from a separate Census source)
    Polling data from a Yale study
    Political voting data from the 2016 Presidential Election
    
In this exercise, I will focus on just the first 3 of these.

Each of the 3 sources has a slightly different way to label a county,
but luckily they all obey the same convention of having a matching numeric
ID for each US state, and a matching ID for each county within the state

The data-cleaning manipulation is 
    converting one format to another
    joining 3 different data frames into one
    removing extra data (for example, state-level, congressional-district level)
    dealing with missing data
    ensuring each of the 3 sources has an index compatible with the other 2
        to facilitate joining

"""

import numpy as np
import pandas as pd

longpath = r"/Users/jonathan/Documents/Documents - Jonathan’s MacBook Pro/MSDS UVA/CS 5010/Project/"

output_csv_filename = longpath + "merged.csv"

# County-level ID:
# format of 'GEOID' or 'STCOU' column is 
# 2-digit state
# plus 3-digit county 
# if it's interpreted as an integer, the leading 0 in the state portion
# may be lost.  So I decided to convert these ID's to strings

# This routine takes an int or str and returns a 
# 5-digit string, adding leading zeroes as needed to reach 5 digits
# It does not expect the input to exceed 5 characters/digits
def padID(id_param):
    id_string = str(id_param)
    if len(id_string) > 5:
        print("ERROR! ID exceeding expected length: " + id_string)
        return id_string
    else:
        return id_string.rjust(5, '0')

# input: 5-character string representing a state/county ID
# returns: false if final 3 digits are all 0's (indicating it's not a county)
#           true otherwise    
def isCountyID(id_string):
    if id_string[2:] == "000":
        return False
    else:
        return True

#######################
# Land-area datasource
#######################
LND_filename = longpath + "LND01.xls"
df_LND = pd.read_excel(LND_filename,
                       usecols = ['Areaname','STCOU','LND010200D'])


# Ensure format of STCOU ID (geographic identifier)
# matches the desired 5-character string format
df_LND['STCOU'] = df_LND['STCOU'].astype('string')
df_LND['STCOU'] = df_LND.apply(lambda x: padID(x['STCOU']), axis = 1)

# Keep only the rows that are for county-level data
df_LND['isCounty'] = df_LND.apply(lambda x: isCountyID(x['STCOU']), axis = 1)
df_LND = df_LND[df_LND.isCounty == True]

# Of these, keep the rows where population > 0
df_LND = df_LND[df_LND.LND010200D > 0]

# Then clean up by removing the column indicating county-hood
df_LND.drop('isCounty', axis=1)

# Set index of df_LND to the geographic ID by which we'll merge dataframes
df_LND.set_index('STCOU', inplace=True)


# Update land areas for known missing values
# Source = Wikipedia (!)
df_LND.at['02230','LND010200D'] = 452  # Skagway, Alaska
df_LND.at['02275','LND010200D'] = 2556  # Wrangell, Alaska
df_LND.at['08014','LND010200D'] = 33 # Broomfield, Colorado


#######################
# Population datasource
#######################
population_filename = longpath + "co-est2019-alldata.csv"
df_POP = pd.read_csv(population_filename, engine = "python", 
                     skiprows = 1,
                     skipfooter = 2,
                     usecols = ['STATE', 'COUNTY', 
                                'POPESTIMATE2019'])
# Use following line to retain additional potentially useful columns
#                     usecols = ['REGION', 'DIVISION', 'STATE', 'COUNTY', 'STNAME', 
#                                'CTYNAME', 'CENSUS2010POP',
#                                'POPESTIMATE2019'])

# for coding convenience, rename population column name
df_POP = df_POP.rename({'POPESTIMATE2019': 'POP'}, axis='columns')

# keep the rows with a non-zero county-id
df_POP = df_POP[df_POP.COUNTY > 0]

def StCouConcat(state_id, county_id):
    # input: state_id, county_id
    # output: STCOU geographic ID in standard form
    s_int = int(state_id)
    c_int = int(county_id)
    return f"{s_int:02}{c_int:03}"

df_POP['STCOU'] = df_POP.apply(lambda x: StCouConcat(x['STATE'],x['COUNTY']), axis = 1)
#df_POP['STCOU'] = StCouConcat(df_POP['STATE'],df_POP['COUNTY'])

#  now that we have the 5-character county ID that's unique across US,
# remove the state-only and county-only columns
df_POP = df_POP.drop('STATE', axis=1)
df_POP = df_POP.drop('COUNTY', axis=1)

# Set index of df_POP to the geographic ID by which we'll merge dataframes
df_POP.set_index('STCOU', inplace=True)


#######################
# Environmental Polling datasource
#######################

YCOM_filename = longpath + "YCOM_2020_Data.csv" 
df = pd.read_csv(YCOM_filename, engine = "python")

# Remove rows that don't contain county data
index_not_county = df[ df['GeoType'] != 'County'].index
df.drop(index_not_county, inplace = True)

# To reduce confusion, remove the population data from this source
# since we discovered it was way outdated
df = df.drop('TotalPop', axis=1)

# Create consistent format for Geographic ID
df['GEOID'] = df.apply(lambda x: padID(x['GEOID']), axis = 1)

df.set_index('GEOID', inplace = True)


###################################
# Merge Land-area, Population, and Environmental Polling data
###################################
df = pd.concat([df, df_LND], axis = 1)
df = pd.concat([df, df_POP], axis = 1)

# Remove a few null values
df = df[~df['GeoType'].isnull()]

df['PopDensity'] = df['POP'] / df['LND010200D']

#########################
# Write the merged file to CSV
#########################
df.to_csv(output_csv_filename, header=True)

