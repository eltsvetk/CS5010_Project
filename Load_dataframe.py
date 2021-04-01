#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 19:35:17 2021

"""

import numpy as np
import pandas as pd
# from datetime import datetime

longpath = r"/Users/jonathan/Documents/Documents - Jonathan’s MacBook Pro/MSDS UVA/CS 5010/Project/"

#----------------------
# This section loads the presidential results
# To-do: rename "final_df" to "political_df" for clarity
# (but that's not done because it's not in Elena's original code)
# Already chaged: I changed "df" to "dfP" to avoid confusion with
# the main dataframe that's also called df

dfP =  pd.read_csv("county_pres.csv")

#rename the "na" candidate votes to "other"
dfP.loc[:,'party'].fillna(value='Other',inplace=True)

#filter to just 2016 presidential election
df_year_2016 = dfP.loc[dfP["year"]== 2016,:]

#filter out the rows where county is a null value
new_df = df_year_2016[df_year_2016['FIPS'].notnull()]

#we dropped 9 null values for county 
#this dataframe will allow you to see the rows I am dropping for context
#these rows do not pertain to a county so we can drop with confidence

null_df = df_year_2016[df_year_2016['FIPS'].isnull()]

#extract just the columns that we need for analysis
new_df_subset = new_df[['FIPS','party','candidatevotes','totalvotes']]

#​#pivot the party column 

final_df = pd.pivot_table(new_df_subset,values='candidatevotes',columns=['party'], index=['FIPS','totalvotes'])
final_df.reset_index(inplace = True)

final_df['FIPS'] = final_df['FIPS'].astype(int)

#add .astype(str) to convert to string


#rename for readability
final_df.rename(columns= {'Other':'other_votes','democrat':'democrat_votes','republican':'republican_votes'}, inplace=True)

#---------------------
# format of 'GEOID' or 'STCOU' column is 2-digit state
# plus 3-digit county 
# if it's interpreted as an integer, the leading 0 in the state portion
# may be lost 
# This routine takes any form (int or str) and returns a 
# 5-digit string, including leading zero if needed
def padID(id_param):
    id_string = str(id_param)
    if len(id_string) == 4:
        return "0" + id_string
    else:
        return id_string

# input: 5-character string representing a state/county ID
# returns: false if final 3 digits are all 0's
#           true otherwise    
def isCountyID(id_string):
    if id_string[2:] == "000":
        return False
    else:
        return True

LND_filename = longpath + "LND01.xls"
df_LND = pd.read_excel(LND_filename,
                       usecols = ['Areaname','STCOU','LND010200D'])
# Format of STCOU includes leading 0's to ensure length of 5

df_LND['STCOU'] = df_LND['STCOU'].astype('string')
df_LND['STCOU'] = df_LND.apply(lambda x: padID(x['STCOU']), axis = 1)

# THIS IS THE NEXT PLACE TO DEBUG
# WE NEED TO DROP THE NON-COUNTIES BECAUSE WE WILL JOIN THE DFs
# AND DON'T WANT THE EXTRA ROWS IN THE RESULTING DF
#LND_index_not_county = df_LND[ ~isCountyID(df_LND['STCOU'])].index
#df_LND.drop(LND_index_not_county, inplace = True)
df_LND.set_index('STCOU', inplace=True)


# Update land areas for known missing values
# Source = Wikipedia (!)
# to be done: note the discrepancy in the report
df_LND.at['02230','LND010200D'] = 452  # Skagway, Alaska
df_LND.at['02275','LND010200D'] = 2556  # Wrangell, Alaska
df_LND.at['08014','LND010200D'] = 33 # Broomfield, Colorado




'''
population_filename = longpath + "co-est2019-alldata.csv"
df_POP = pd.read_csv(population_filename, engine = "python", 
                     skiprows = 1,
                     skipfooter = 2,
                     usecols = ['REGION', 'DIVISION', 'STATE', 'COUNTY', 'STNAME', 
                                'CTYNAME', 'CENSUS2010POP',
                                'POPESTIMATE2019'])
'''

YCOM_filename = longpath + "YCOM_2020_Data.csv" 
df = pd.read_csv(YCOM_filename, engine = "python")



# Remove rows that don't contain county data
# (this may be too extreme -- we might want to keep the non-county data)
index_not_county = df[ df['GeoType'] != 'County'].index
df.drop(index_not_county, inplace = True)

# format of 'GEOID' column is state+county but without leading 0's
# ensure GEOID is a string, and add leading zero if needed
def padID(id_param):
    if len(id_param) == 4:
        return "0" + id_param
    else:
        return id_param
    
df['GEOID'] = df['GEOID'].astype('string')
df['GEOID'] = df.apply(lambda x: padID(x['GEOID']), axis = 1)
df.set_index('GEOID', inplace = True)

'''
# remove rows from Census Population data with County == 0, since
# These are state-level data
index_state_data = df_POP[ df_POP['COUNTY'] == 0].index
df_POP.drop(index_state_data, inplace = True)
'''

'''
#old version
def getLandArea(stcou_concat):
    answerSeries = df_LND.loc[df_LND['STCOU'] == int(stcou_concat)]['LND010200D']
    try:
        ret_val = answerSeries.values[0]
    except IndexError:
        ret_val = -1
    finally:
        return ret_val
'''
def getLandArea(stcou_concat):
    print("checking " + stcou_concat)
    return df_LND.at[str(stcou_concat), 'LND010200D']
    #answerSeries = df_LND.loc[df_LND['STCOU'] == int(stcou_concat)]['LND010200D']
    #try:
    #    ret_val = answerSeries.values[0]
    #except IndexError:
    #    ret_val = -1
    #finally:
    #    return ret_val

def getLandArea2inputs(state_id, county_id):
    # input: state_id, county_id
    # output: land area
    stcou_concat = f"{state_id:02}{county_id:03}"
    print("checking " + stcou_concat)
    return getLandArea(stcou_concat)


def calcPopDensity(people_count, land_count):
    if land_count == 0:
        print("Error: calcPopDensity with zero land area. People = " + str(people_count))
        return -1
    else:
        return people_count / land_count

'''
# This one may be unnecessary if the effort below to 
# put everything into the main df succeeds
df_POP['LANDAREA'] = df_POP.apply(lambda x: getLandArea2inputs(x['STATE'], x['COUNTY']), axis = 1)
'''

# add column 'LANDAREA' = county's land area in square miles
#df['LandArea'] = df.apply(lambda x: getLandArea(x['GEOID']), axis = 1)
df3 = pd.concat([df, df_LND], axis = 1)

#df['PopDensity'] = df.apply(lambda x: calcPopDensity(x['TotalPop'], x['LandArea']), axis = 1)








'''
# filtered version of df with only state-level data
is_state = df['GeoType']=='State'
df_state = df[is_state]

# filtered version of df with only county-level data
is_county = df['GeoType']=='County'
df_county = df[is_county]

# Create a dictionary to translate from State Code to State Name
statename = pd.Series(df_state.GeoName.values,index=df_state.GEOID).to_dict()
# now a call of statename[6] returns 'California'


# Input: County ID
# Output: state ID
def stateFromCountyGeoID (full_geoid):
    # a full geoid has 4 or 5 digits.
    # The final 3 digits are the county ID
    # The first 1 or 2 digits are the state ID
    if len(str(full_geoid)) == 4:
        stateID = str(full_geoid)[0:1]
    elif len(str(full_geoid)) == 5:
        stateID = str(full_geoid)[0:2]     
    else:
        print("ERROR: full_geoID of unexpected length: " + str(full_geoid))
    return stateID

# Add StateID column to the county-only dataframe
df_county['StateID'] = df_county.apply(lambda x: stateFromCountyGeoID(x['GEOID']), axis = 1)
df_county['StateID'] = df_county['StateID'].astype(int)

# Add StateName column to the county-only dataframe
df_county['StateName'] = df_county['StateID'].map(statename)
'''
