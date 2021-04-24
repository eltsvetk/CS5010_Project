# -*- coding: utf-8 -*-
"""
Elena Tsvetkova

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.graphics.gofplots import ProbPlot
from statsmodels.stats.outliers_influence import variance_inflation_factor


df = pd.read_csv("merged.csv", index_col=0)

#Data Exploration

#Question:
#do the people who think global warming is happening also think a candidate's views 
#on global warming are important to their vote?
#How does this relate to the candidate of choice from the 2016 presidential election?
#How does this relate to counties with smaller population densities vs larger population densities

#comparing % who think global warming is happening vs
#% who say a candidate's views on global warming are important to their vote

#adding column
df['%Democrat'] = (df['democrat_votes'] / df['totalvotes']) * 100
df['%Republican'] = (df['republican_votes'] / df['totalvotes']) * 100
df['Abs_Difference'] = df['%Democrat'] - df['%Republican']
df['Abs_Difference'] = df['Abs_Difference'].abs()

df['Political_Affiliation'] = np.where(
    df['Abs_Difference'] < 2, 'Swing', np.where(
    df['%Democrat'] >  df['%Republican'], 'Demo', 'Repub')) 

df.rename(columns = {'PopDensity': 'PopDensity (pop/sq mi)'}, inplace = True)

df.to_csv("merged_columns_added_renamed.csv")

sns.set(style="darkgrid")

gfg = sns.scatterplot(x='happening', y='priority', data=df, hue='Political_Affiliation', palette=['red','blue','green'],
                size='PopDensity (pop/sq mi)', sizes=(10, 500),alpha=.5)
 
#plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
plt.setp(gfg.get_legend().get_texts(), fontsize='9')  
  
# for legend title
#plt.setp(gfg.get_legend().get_title(), fontsize='100')  
plt.xlabel("% who think GW is happening")
plt.ylabel("%who priortize candidates views on GW")
plt.title("%Who think GW is happening vs those who care")
plt.tight_layout()
plt.savefig('scatterplot.png', dpi=300)
plt.show()

#There appears to be a linear relationship between the % of those who believe GW is happening
#vs those who prioritize their candidate's views on GW 

#However, it is interesting how there is about a 15-20% difference between those who think GW is 
#happening and those who prioritize candidate views on GW
#In other words, 85% could believe it is happening but only 70% prioritize candidate views 
#on GW

#What is the correlation between those who think GW is happening and those who
#prioritize candidate's views on GW?

df.loc[:,['happening','priority']].corr() #default is pearson

#The correlation is 0.925421. This correlation is close to 1 which implies that the relationship
#between those who think GW is happening and those who prioritize candidate's views on GW
#is linear. However, correlation must be interpreted with scatterplot to ensure correlation
#is reliable

sns.set(style="darkgrid")
sns.regplot(x='happening', y='priority', data=df, marker='+') #will provide a line of best fit as well
plt.title("%Who think GW is happening vs Priority on GW")
plt.savefig('regplot.png', dpi=300)

#Box plot  - %GW is happening
sns.set(style="darkgrid")
my_pal = {'Demo':'blue', 'Repub':'red', 'Swing':'green'}
sns.boxplot(x=df['Political_Affiliation'],y=df['happening'],palette=my_pal)
plt.title("GW is happening vs Political Affiliation")
plt.savefig('boxplot1.png', dpi=300)
plt.show()

#The average % of those who think GW is happening is highest for democratic counties when 
#comparing to republican and swing counties

#Box plot - %prioritize candidate's views on GW
sns.set(style="darkgrid")
my_pal = {'Demo':'blue', 'Repub':'red', 'Swing':'green'}
sns.boxplot(x=df['Political_Affiliation'],y=df['priority'],palette=my_pal)
plt.title("Candidate's views on GW is Priority vs Political Affiliation")
plt.savefig('boxplot2.png', dpi=300)
plt.show()

#The average % of those who prioritize their candidate's views on GW is highest for 
#democratic counties when comparing to republican and swing counties

#It appears from the box plots that swing is typically in the middle range when 
#comparing republican vs democrat views - which makes sense!


#First, let's perform a simple linear regression model where our response variable is
#those who prioritize candidate's views on GW and the predictor variable is whose who
#think GW is happening

#from our scatterplot with the linear regression model fit, the points appear to not be
#scattered evenly or have a constant vertical spread when the % of those who think GW
#is happening is around the 50-55% range and 80-85% range

#Simple linear model (least squares regression):
   
#one way to build model is using scipy stats
#convert select columns to array
#response = df.loc[:,'priority'].values
#predictor = df.loc[:,'happening'].values
#model = stats.linregress(x=predictor, y=response)


#Another way to build model is using ols from statsmodels
#code obtained and adjusted from:
#https://www.pythonfordatascience.org/anova-python/

model = ols('priority ~ happening',data=df).fit()
model.summary()

#ANOVA F test
aov_table = sm.stats.anova_lm(model, typ=2)
aov_table

#Our p-value for our F statistic is less than alpha=0.05, indicating that we reject our null
#hypothesis. Data supports the claim that a linear relationship exists between those who
#prioritize candidate's view on GW and thos who think GW is happening. 

#the equation is 
#priority = -25.4896 + 1.0688*happening

#Our R^2 is 0.856. So, 85.6% of the variability in the % of those who prioritize
#candidate's views on GW (y) can be explained by the regression model

#Check Assumptions

#code obtained and adjusted from:
#https://robert-alvarez.github.io/2018-06-04-diagnostic_plots/

model_fitted = model.fittedvalues
model_residuals = model.resid

plot_resid = plt.figure()
plot_resid.axes[0] = sns.residplot(x=model_fitted, y=model_residuals, data=df,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_resid.axes[0].set_title('Residuals vs Fitted')
plot_resid.axes[0].set_xlabel('Fitted values')
plot_resid.axes[0].set_ylabel('Residuals');
plt.savefig('residplot_beforeTrans.png', dpi=300)

#the assumption for constant variance and residuals having mean 0 does not appear to be met
#since both of these assumptions are violated, we will transform the y variable

df['trans_y'] = np.log(df['priority'])

trans_model = ols('trans_y ~ happening',data=df).fit()

trans_model_fitted = trans_model.fittedvalues
trans_model_resid = trans_model.resid

plot_resid_2 = plt.figure()
plot_resid_2.axes[0] = sns.residplot(x=trans_model_fitted, y=trans_model_resid, data=df,                         
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_resid_2.axes[0].set_title('Residuals vs Fitted')
plot_resid_2.axes[0].set_xlabel('Fitted values')
plot_resid_2.axes[0].set_ylabel('Residuals');
plt.savefig('residplot_afterTrans.png', dpi=300)

#our assumption for residuals having mean 0 is met. Our assumptions for residuals having
#constant is close to met!

#Normality assumption:

#normalized residuals - after transforming
model_norm_resid = trans_model.get_influence().resid_studentized_internal

qq = ProbPlot(model_norm_resid)
plot_qq = qq.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)
plot_qq.axes[0].set_title('Normal Q-Q - After transforming')
plot_qq.axes[0].set_xlabel('Theoretical Quantiles')
plot_qq.axes[0].set_ylabel('Standardized Residuals');
plt.savefig('QQplot_afterTrans.png', dpi=300)

#normalized residuals - before transforming
model_norm_resid_2 = model.get_influence().resid_studentized_internal

qq_2 = ProbPlot(model_norm_resid_2)
plot_qq_2 = qq_2.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)
plot_qq_2.axes[0].set_title('Normal Q-Q - Before transforming')
plot_qq_2.axes[0].set_xlabel('Theoretical Quantiles')
plot_qq_2.axes[0].set_ylabel('Standardized Residuals');

#After transforming, the points appear to be on the straight line much more
#normality assumption is met (residuals appear to follow a normal distribution)

#Independence assumption

#We know that our groups are mutually exclusiv
#data is not repeated measures (not collected through time)
#so, the independence assumption is met

#do we have any leverage points?
#Will use Cook's distance

#Residuals vs Leverage plot

# leverage, from statsmodels internals
model_lev = trans_model.get_influence().hat_matrix_diag
# cook's distance, from statsmodels internals
model_cooks = trans_model.get_influence().cooks_distance[0]

plot_lev = plt.figure();
plt.scatter(model_lev, model_norm_resid, alpha=0.5);
sns.regplot(model_lev, model_norm_resid,
              scatter=False,
              ci=False,
              lowess=True,
              line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8});
plot_lev.axes[0].set_xlim(0, max(model_lev)+0.01)
plot_lev.axes[0].set_ylim(-3, 5)
plot_lev.axes[0].set_title('Residuals vs Leverage')
plot_lev.axes[0].set_xlabel('Leverage')
plot_lev.axes[0].set_ylabel('Standardized Residuals');
plt.savefig('Cooksdistance_afterTrans.png', dpi=300)

#all of the Cook's distance measures for the data points are less than 0.5
#no data points are influential

#We will continue with our transformed model!



trans_model.summary()

#Question:
#Is the %of those who think GW is happening a significant predictor
#for the % of those who prioritize candidate's views on GW?

#note that our R^2 has increased slightly
#Our R^2 is 0.862. So, 86% of the variability in the % of those who prioritize
#candidate's views on GW (y) can be explained by the regression model when
#y is transformed by the natural log

#the coefficient is 0.0234. (exp(0.0234) – 1) * 100 = 2.368. 
#For every 1% increase in the % of those who think GW is happening,
#the % of those who prioritize candidate's views on GW increases by about 2.4%.

##Example:
#So, if the % of those who think GW happening increased by 1% from 60% (to 61%),
#then the % of those who prioritize candidate's views on GW increases
#from 50% to 50%+(50%*2.4%) or 51.2%.

#Lets try a model with categorical variable: Poltical Affiliation

df['polt_dummy']=df.Political_Affiliation.map({'Demo':1,'Repub':2,'Swing':3})

y = df['priority']
x = df[['happening','polt_dummy']]

#to avoid dummy trap: one variable can be predicted from the others
x = pd.get_dummies(data=x, drop_first=True)

trans_model_cat = ols('trans_y ~ happening + C(polt_dummy)', data=df).fit() 

trans_model_cat.summary()

#our adjusted R^2 is 86.7%

#Democratic votes from 2016 election is the reference class

#the coefficient is Repub indicator variable is -.0387
#(exp(-.0387) – 1) * 100 = -3.796

#The % of those who prioritize candidate's views on GW
#decreases on average by about 3.8% per change in the % of those
#who think GW is happening if they voted Republican in 2016
#election relative to if they voted Democrat

#How does population density relate to climate change?
#first, we checked by adding population density to the model above but
#it was not a significant predictor to the %of those who prioritize
#candidates views on GW when the other variables are in the model

#Therefore, we changed our response variable.

#Question:
#What is the relationship between those who think global warming is
#happening and those who are actually worried and what is the relationship
#with population density?

sns.set(style="darkgrid")

gfg = sns.scatterplot(x='happening', y='worried', data=df,
                size='PopDensity (pop/sq mi)', sizes=(10, 500),alpha=.5)

#plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
plt.setp(gfg.get_legend().get_texts(), fontsize='9')  
  
# for legend title
#plt.setp(gfg.get_legend().get_title(), fontsize='100')  
plt.xlabel("% who think GW is happening")
plt.ylabel("%who are worried")
plt.title("%Who think GW is happening vs those who are worried")
plt.tight_layout()
plt.savefig('scatterplot.png', dpi=300)
plt.show()

#There appears to be a linear relationship between the % of those who believe GW is happening
#vs those who are worried
#population density also seems to have a relationship 

#What is the correlation between those who think GW is happening and those who
#are worried?

df.loc[:,['happening','worried']].corr() #default is pearson
df.loc[:,['PopDensity','worried']].corr()

#The correlation is 0.94919. This correlation is close to 1 which implies that the relationship
#between those who think GW is happening and those who are worried
#is linear.

#What is the correlation between population density and those who
#are worried?

df.loc[:,['PopDensity (pop/sq mi)','worried']].corr()

#the correlation is 0.307285
#This is considered a weak relationship but it does not mean that no relationship exits


#let's perform a simple linear regression model with population density as a 
#predictor

df.rename(columns = {'PopDensity (pop/sq mi)': 'PopDensity'}, inplace = True)

model_pop = ols('worried ~ happening + PopDensity',data=df).fit()
model_pop.summary()

#the predictor variables happening and PopDensity appear to be 
#significant predictors (when alpha=0.05) to predict % those who are worried

#Our adjusted R^2 is .903. So, 90.3% of the variability in the % of those who are worried
#about GW can be explained by the regression model

#Check our assumptions:
    
#residual plot

model_fitted_pop = model_pop.fittedvalues
model_residuals_pop = model_pop.resid

plot_resid_pop = plt.figure()
plot_resid_pop.axes[0] = sns.residplot(x=model_fitted_pop, y=model_residuals_pop, data=df,
                          lowess=True,
                          scatter_kws={'alpha': 0.5},
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_resid_pop.axes[0].set_title('Residuals vs Fitted')
plot_resid_pop.axes[0].set_xlabel('Fitted values')
plot_resid_pop.axes[0].set_ylabel('Residuals');
plt.savefig('residplot_popdens.png', dpi=300)

#the assumption for residuals having constant variance appears to be met
#the assumption for residuals having mean zero appears to be met

#QQ plot

model_norm_resid_pop = model_pop.get_influence().resid_studentized_internal

qq_pop = ProbPlot(model_norm_resid_pop)
plot_qq_pop = qq.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)
plot_qq_pop.axes[0].set_title('Normal Q-Q - After transforming')
plot_qq_pop.axes[0].set_xlabel('Theoretical Quantiles')
plot_qq_pop.axes[0].set_ylabel('Standardized Residuals');
plt.savefig('QQplot_afterTrans.png', dpi=300)

#normality assumption is met (residuals appear to follow a normal distribution)

#Independence assumption

#We know that our groups are mutually exclusiv
#data is not repeated measures (not collected through time)
#so, the independence assumption is met

model_pop.summary()

#coefficient for happening is 0.9885
#.99% is the expected change in the % of those are worried per a 
#1% change in those who think GW is happening when population
#density is held constant

#coefficient for pop density is .0002
#.0002% is the expect change in the % of those who are worried per
#unit change in the population/sq mi (population density) when
#the % of those who GW is happening is held constant


#To check, is there any multicollinearity between our predictor variables?
#code obtained and adjusted from https://www.geeksforgeeks.org/detecting-multicollinearity-with-vif-python/

# the independent variables set
X = df[['happening', 'PopDensity']].dropna()
  
# VIF dataframe
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
  
# calculating VIF for each feature
vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]
  
print(vif_data)

#The VIF's are below 10, we do not have any signs on multicollinearity for our model











