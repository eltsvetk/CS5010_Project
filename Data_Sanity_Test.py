#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Confirm that Project Data is reasonable

"""

import numpy as np
import pandas as pd

longpath = r"/Users/jonathan/Documents/Documents - Jonathan’s MacBook Pro/MSDS UVA/CS 5010/Project/"

input_csv_filename = longpath + "merged.csv"

df = pd.read_csv(input_csv_filename)

# Check that total land area is ROUGHLY correct
# Using external data source, without an expectation of an exact match
# Wikipedia says: 3.8 MM square miles.
total_land_data = df['LND010200D'].sum()
total_land_wikipedia = 3797000
total_land_gap_pct = 100*abs((total_land_data - total_land_wikipedia) / total_land_data)
print("gap between Wikipedia and our land area data:")
print('{:,.2}%'.format(total_land_gap_pct))

# Check that total population is ROUGHLY correct
# Wikipedia says: 3.8 MM square miles.total_land_data = df['LND010200D'].sum()
total_pop_wikipedia = 328000000 #2019 estimate
total_pop_data = df['POP'].sum()
total_pop_gap_pct = 100*abs((total_pop_data - total_pop_wikipedia) / total_pop_data)
print("gap between Wikipedia and our population data:")
print('{:,.2}%'.format(total_pop_gap_pct))

# Check total votes in 2016 Pres Election
# Source: https://en.wikipedia.org/wiki/2016_United_States_presidential_election
total_Clinton_w = 65853514
total_Trunp_w = 62984828
total_Clinton_data = df['democrat_votes'].sum()
total_Trump_data = df['republican_votes'].sum()
total_Clinton_gap_pct = 100*(total_Clinton_data - total_Clinton_w) / total_Clinton_w
print("gap between Wikipedia and our Clinton voter data:")
print('{:,.2}%'.format(total_Clinton_gap_pct))

total_Trump_gap_pct = 100*(total_Trump_data - total_Trunp_w) / total_Trunp_w
print("gap between Wikipedia and our Trump voter data:")
print('{:,.2}%'.format(total_Trump_gap_pct))

# Confirm there are no duplicated county names
import collections
counter = collections.Counter(df['GeoName'])
for x in counter:
    value = counter[x]
    if value > 1:
        print("Error: duplicate Geoname found")
        print(value)


