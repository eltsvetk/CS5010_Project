#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Clean sources of data for CS5010 Project 
Climate Change Attitudes
Merge them into a single dataframe
Export that dataframe to CSV

"""

import numpy as np
import pandas as pd

#longpath = r"/Users/jonathan/Documents/Documents - Jonathan’s MacBook Pro/MSDS UVA/CS 5010/Project/"

#be sure your working directory is referencing the top level of 
# github repository CS5010_Project
longpath = "project_data_prep/datasets/"

# Source Data filenames
Pres_filename = longpath + "county_pres.csv"  # Presidential vote by county
population_filename = longpath + "co-est2019-alldata.csv" # US Census Population
LND_filename = longpath + "LND01.xls"  # Land area by county
YCOM_filename = longpath + "YCOM_2020_Data.csv"   # Yale university polling data

# 206 Swing Counties scraped from:
# https://ballotpedia.org/List_of_Pivot_Counties_-_the_206_counties_that_voted_Obama-Obama-Trump
# They voted for Obama both times, then for Trump in 2016
Swing_county_filename = longpath + "SwingCounties.csv"   

# This is the file the rest of the project will use
# for statistical analysis and mapping data:
output_csv_filename = longpath + "merged.csv"


# Routines to process the key geographic ID we'll use
# To stitch together the 4 data sources

# County-level ID:
# format of 'GEOID' or 'STCOU' column is 
# 2-digit state
# plus 3-digit county 
# if it's interpreted as an integer, the leading 0 in the state portion
# may be lost.  So we decided to convert these ID's to strings

# Input: an int, floating point, or string containing numeric characters
# Output: 5-digit numeric string, adding leading zeroes as needed to reach 5 digits
# It expects the input not to exceed 5 characters/digits
def padID(id_param):
    id_string = str(int(id_param))
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
# Presidential Results datasource
#######################

dfP =  pd.read_csv(Pres_filename)

#rename the "na" candidate votes to "other"
dfP.loc[:,'party'].fillna(value='Other',inplace=True)

#filter to just 2016 presidential election
#df_year_2016 = dfP.loc[dfP["year"]== 2016,:]
dfP = dfP[dfP.year == 2016]

#filter out the rows where county is a null value
#new_df = df_year_2016[df_year_2016['FIPS'].notnull()]
dfP = dfP[dfP['FIPS'].notnull()]

#we dropped 9 null values for county 
#this dataframe will allow you to see the rows I am dropping for context
#these rows do not pertain to a county so we can drop with confidence
#null_df = df_year_2016[df_year_2016['FIPS'].isnull()]

# Ensure format of FIPS (geographic identifier)
# matches the desired 5-character string format
dfP['FIPS'] = dfP.apply(lambda x: padID(x['FIPS']), axis = 1)

#extract just the columns that we need for analysis
new_df_subset = dfP[['FIPS','party','candidatevotes','totalvotes']]

#​#pivot the party column 
dfP = pd.pivot_table(new_df_subset,values='candidatevotes',columns=['party'], index=['FIPS','totalvotes'])
dfP.reset_index(inplace = True)

#rename columns for readability
dfP.rename(columns= {'Other':'other_votes','democrat':'democrat_votes','republican':'republican_votes'}, inplace=True)

# republican (ie, Trump) percentage of total votes
dfP['republican_pct'] = round(dfP['republican_votes'] / dfP['totalvotes'],4)


#######################
# Swing County datasource 
#######################
dfSwing =  pd.read_csv(Swing_county_filename)
dfSwing['Swing'] = True

# Ensure format of FIPS (geographic identifier)
# matches the desired 5-character string format
dfSwing['FIPS'] = dfSwing.apply(lambda x: padID(x['FIPS']), axis = 1)

#Remove unneeded columns
del dfSwing['County']
del dfSwing['State']
del dfSwing['Full Name']

# Add Swing data into dfP
dfP = dfP.join(dfSwing.set_index('FIPS'), on='FIPS')

# Set index to the geographic ID by which we'll merge dataframes
dfP.set_index('FIPS', inplace=True)


#######################
# Land-area datasource
#######################

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
df = pd.concat([df, dfP], axis = 1)

# Remove a few null values
df = df[~df['GeoType'].isnull()]

# Calculate value for population density
df['PopDensity'] = df['POP'] / df['LND010200D']

# Calculate scaled population density (40 to 80) for 
# ease of display in Heroku
# Scaling Formula:
# log(PopDensity) * ScalingFactor + ScaleMin
# ScaleMin is set to 40 so that color display in Heroku
# will work well for both Pop Density (within 40-90 range)
# and for polling results (which also fall in the 40-90 range)
ScaleMax = 90
ScaleMin = 40
ScaleRange = ScaleMax - ScaleMin
PopMax = df['PopDensity'].max()
ScalingFactor = ScaleRange / np.log(PopMax)
LogPad = 3 # add this constant to Pop Density
            # To avoid log of PopDensity from going below zero

df['ScaledPopDensity'] = (np.log(df['PopDensity']+LogPad) * 
                          ScalingFactor +
                          ScaleMin)

###################################
# Add Columns for Stats and Plotting Convenience
###################################
df['%Democrat'] = (df['democrat_votes'] / df['totalvotes']) * 100
df['%Republican'] = (df['republican_votes'] / df['totalvotes']) * 100

def label_party_color(row):
    if row['Swing'] == True:
        return 'Swing'
    if (row['%Democrat'] > row['%Republican']) :
        return 'Demo'
    return 'Repub'

df['Political_Affiliation'] = df.apply(lambda 
                                       row: label_party_color(row),
                                       axis = 1)


df.rename(columns = {'PopDensity': 'PopDensity (pop/sq mi)'}, inplace = True)


#########################
# Remove unneeded columns then
# Write the merged file to CSV
#########################
del df['GeoType']
del df['Swing']
df.to_csv(output_csv_filename, header=True)

