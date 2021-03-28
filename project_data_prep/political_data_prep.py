# -*- coding: utf-8 -*-
"""
Data prep for project 

"""

import pandas as pd

df =  pd.read_csv("county_pres.csv")

#filter to just 2016 presidential election
df_year_2016 = df.loc[df["year"]== 2016,:]

#rename the "na" candidate votes to "other"
df_year_2016['party'].fillna(value='Other', inplace = True)

#filter out the rows where county is a null value
new_df = df_year_2016[df_year_2016['FIPS'].notnull()]

#we dropped 9 null values for county 
#this dataframe will allow you to see the rows I am dropping for context
#these rows do not pertain to a county so we can drop with confidence

null_df = df_year_2016[df_year_2016['FIPS'].isnull()]

#extract just the columns that we need for analysis
new_df_subset = new_df[['FIPS','party','candidatevotes','totalvotes']]

#pivot the party column 

final_df = pd.pivot_table(new_df_subset,values='candidatevotes',columns=['party'], index=['FIPS','totalvotes'])
final_df.reset_index(inplace = True)

final_df['FIPS'] = final_df['FIPS'].astype(int)

#add .astype(str) to convert to string


#rename for readability
final_df.rename(columns= {'Other':'other_votes','democrat':'democrat_votes','republican':'republican_votes'}, inplace=True)

