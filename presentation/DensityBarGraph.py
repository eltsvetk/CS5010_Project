#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Create Bar Graph showing effect of Pop Density
on attitudes about climate change

For Conclusion of presentations

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#be sure your working directory is referencing the top level of github repository CS5010_Project

longpath = "project_data_prep/datasets/"

csv_filename = longpath + "merged.csv"

df = pd.read_csv(csv_filename)

# create a list of our conditions
conditions = [
    (df['PopDensity (pop/sq mi)'] > 500) & (df['Political_Affiliation'] == 'Demo'),
    (df['PopDensity (pop/sq mi)'] <= 500) & (df['Political_Affiliation'] == 'Demo'),
    (df['PopDensity (pop/sq mi)'] > 500) & (df['Political_Affiliation'] == 'Repub'),
    (df['PopDensity (pop/sq mi)'] <= 500) & (df['Political_Affiliation'] == 'Repub')
    ]

# create a list of the values we want to assign for each condition
values = ['Denser Dem', 'Sparser Dem', 'Denser Rep', 'Sparser Rep']

df['DensityGroup'] = np.select(conditions,values)

df_grouped = df.groupby('DensityGroup', axis=0).mean()[['happening','worried','priority']]

# The following is an awkward/inelegant way to create the data arrays
# needed for the bar graph.
# I'm sure this could be done with a single line of Python code,
# but there are only so many hours in the day to play around with 
# new tricks
DenseDvals = [df_grouped['happening'].values[1],
              df_grouped['worried'].values[1],
              df_grouped['priority'].values[1]]

DenseRvals = [df_grouped['happening'].values[2],
              df_grouped['worried'].values[2],
              df_grouped['priority'].values[2]]

SparseDvals = [df_grouped['happening'].values[3],
              df_grouped['worried'].values[3],
              df_grouped['priority'].values[3]]

SparseRvals = [df_grouped['happening'].values[4],
              df_grouped['worried'].values[4],
              df_grouped['priority'].values[4]]


# define figure
fig, ax = plt.subplots(1, figsize=(8, 6))

# numerical x
x = np.arange(0, 3)

# plot bars
# To produce the 2-bar plot, comment out the 2nd and 4th bars
# To produce the 4-bar lot, use all four of the following lines:
plt.bar(x - 0.2, SparseRvals, width = 0.1, color = 'red')
#plt.bar(x - 0.1, DenseRvals, width = 0.1, color = 'firebrick')
plt.bar(x + 0.1, SparseDvals, width = 0.1, color = 'royalblue')
#plt.bar(x + 0.2, DenseDvals, width = 0.1, color = 'darkblue')


# remove spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# x y details
plt.ylabel('Percent of respondents')
plt.xticks(x, ['Is GW Happening?','Are You Worried?','Is it a Priority?'])

# grid lines
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.ylim(20,90)

# title and legend
plt.title('Correlation of Population Density and Climate Change Attitude', loc ='left')
plt.legend(['Low-Density\nRepublican\nCounties',  
            'Low-Density\nDemocratic\nCounties'], loc='upper left', ncol = 4)
plt.show()
