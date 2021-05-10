# U.S. Climate Change Attitudes

Term Project for CS5010, Spring 2021

Group 4: Elena Tsvetkova (rrm3nh@),  Anita Taucher (agt4vw@), and Jonathan Shakes (hqe7rd@)

## INTRODUCTION
We set out to answer a hypothesis: climate-change-related attitudes in cities will be significantly different than those in rural areas. This topic area is interesting, because around the world, humans are migrating towards cities. If people in cities “lose touch” with the importance of protecting the environment, that would have implications for environmental health, especially in a democracy like the U.S., where voters ultimately decide whether to enact and enforce laws that limit destruction of the natural world. Without such legal protection, the environment suffers due to what economists call "negative externalities" and the "tragedy of the commons." 

To study this topic, we needed public-opinion data about environmental data, with a distinction between people living in city and rural areas.

## THE DATA
Prior to beginning studies at UVA, Jonathan learned about climate-change-related survey data during volunteer work he did with Citizens’ Climate Lobby (CCL) (Note 1). Anita and Elena shared Jonathan’s interest in the general topic. CCL uses the survey data as part of its grass-roots mobilization within the US. Understanding what voters believe about climate change policy is an important piece of data to inform effective grass-roots advocacy.

Our core data set comes from the Yale Program on Climate Change Communications (Notes 2, 3). The Yale data contains multi-year results from surveys in the U.S.. Our data file from Yale consists of about 5000 rows, each corresponding to a geographic area, and several dozen columns with responses to questions like, “Do you think climate change is happening,” or “Do you think your state's governor should do more about climate change?”  These surveys were administered from 2018 to 2020. The sample size is large enough to support results broken out at the level of U.S. counties and congressional districts, opening the possibility for us to do map-based geographic analysis.

We decided that looking at the data through the lens of the urban/rural divide, using population density as a numeric indicator, might add value to this existing data set.  In an FAQ for the dataset, we discovered that the data’s relation with population density is both of general interest and not something that has been done before (Note 4).  The potential to look at less-traveled territory made our project more interesting to us, even though we’re realistic enough to understand that our class project is unlikely to break serious new ground, from an academic perspective.

The survey data was limited to the US. While the climate change problem is a global one,  the data was so valuable and relevant that we decided to center our work on it.

At the finest level of detail, the Yale data is split by county and congressional district.  We chose to focus on county, not congressional district, because there are nearly six times as many counties as congressional districts, and therefore our maps might show finer gradations in degree as population density drops in correlation with the distance from the densest cities.

The population and land-area at the county-level were each obtained in separate files from the US Census Bureau (Notes 5, 6).  By matching these two files together, dividing population by land area, we calculated the population density per square mile of land for each county or county-equivalent geographic portion of the U.S.. 

We also assembled the 2016 presidential election returns for each county in the US from the Election Lab at MIT (Note 7). By looking at the vote totals in each county, we could categorize each county as Republican or Democratic. That was an important step for our study, because political preferences are commonly known to be linked to climate change attitudes. Political data was not included in the Yale dataset, but it helped us determine whether population density had any significant correlation with climate-change attitudes, beyond what political preferences alone would predict.

Finally we scraped yet another web data source, Ballotpedia, to identify a list of 206 “swing counties” in the US where a majority of voters voted for Obama in 2008 and 2012, then swung Republican in 2016, voting for Donald Trump (Note 8).  The entire list of swing counties was visible on a single web page, so scraping was a simple matter of identifying the correct chunk of HTML and then removing the extraneous tags and data.  Note: This portion of our work went beyond the basic requirements of the project.

## EXPERIMENTAL DESIGN
### Data Preparation
In order to merge these five separate sources into a single data frame, we

* Loaded each one into a Pandas dataframe,
* Removed non-county-level data
* Converted each file’s incompatible county indicator into a common, 5-digit ID number, based on the US State (2 digits) and county name (3 digits).
* Filled in a half-dozen data rows, missing from the US Census data, using separate web research. The population of these counties was small enough that removing them from the dataset would not have given significantly different results.  
* Set the county ID as the index for each dataframe
* Merged all data frames into a single dataframe
* Derived data for a few new columns such as population density and political categorizations, for convenience and uniform handling in the subsequent processing scripts.  
* Exported the dataframe to a new CSV file that could be used as input to our statistical analysis script and our interactive map-making script.

### Data Exploration
We performed exploratory data analysis utilizing the _Seaborn_ library to investigate a relationship between climate change attitudes, political affiliation, and population density. We also obtained a correlation coefficient to further investigate the existence of a linear relationship between these variables. Based on the results from the exploratory analysis, we built two models described below. 
We focused on the following variables, broken out by county: 
1. Percent of respondents who think global warming is happening
2. Percent of respondents who prioritize their votes based on candidate’s views on global warming
3. Political affiliation (whether county voted majority Democratic, Republican, or Swung from Democratic to Republican in the 2016 presidential election)
4. Percent of respondents who are worried about global warming
5. Population density per square mile

The variables above were used to allow us to answer the following two questions:

1. Do the people who think global warming is happening also think a candidate's views on global warming are important to their vote and how does this relate to the candidate of choice from the 2016 presidential election?
2. What is the relationship between those who think global warming is happening and those who are actually worried and what is the relationship with population density?

**Note:** the _statsmodels_ library was utilized to perform various tasks described below, ranging from the model building itself to acquiring the Variance Inflation Factors (VIFs). The statistical analysis described below (along with transformations) goes beyond the basic requirements of the project.

### First Model
Our first model had the percentage of those who prioritize candidate’s views on global warming as the response with 2 predictor variables: those who think global warming is happening (a continuous variable) and the results from the 2016 presidential election (categorical variable). 

Initially, we looked at the simple linear model with only 1 predictor variable, those who think global warming is happening, to correct for any assumptions not being met. We found that two assumptions for linear regression were not met: the assumption for constant variance and residuals having mean 0. Since both of these assumptions were violated, we log transformed the y variable (response). Afterward, our assumptions for residuals having constant variance and mean 0 were met. In addition, the normality assumption improved after transforming the y variable. With regards to the independence assumption, we noted that it was met because we know that our groups are mutually exclusive (not repeated measures or collected through time). 

Lastly, we used Cook’s distance to identify any leverage points. We found no data points that were influential. Once all of the assumptions for a linear regression model were met, we added the categorical variable into the model. Note that the democratic votes from the 2016 presidential election was the reference class. To evaluate our model performance, we utilized the adjusted R squared for the model (to obtain the percentage variability captured by the model), the p-value for the F statistic for the overall model (to see if the data supported the claim that there was a linear relationship between the response and predictors), and the p-value for the t statistic for each predictor variable (to see if the predictor provided value to the overall model performance). 

Note that we did add population density to this model to see whether it provided value to its predictive ability. However, it was not a significant predictor to the % of those who prioritize candidate’s views on global warming when the other predictors were in the model.

### Second Model
Our second model had the percentage of those who are worried about global warming as the response with 2 predictor variables: those who think global warming is happening (a continuous variable) and population density (a continuous variable). Within our second model, we found that all of the assumptions for linear regression (normality, independence, residuals having constant variance and mean 0) were met. No transformations were required. 

In this model, since our two predictor variables were continuous, we found the Variance Inflation Factor (VIF) for each feature to check for multicollinearity. Once again, to evaluate our model performance, we utilized the adjusted R squared for the model, the p-value for the F statistic for the overall model, and the p-value for the t statistic for each predictor variable.

## RESULTS

### Data Exploration Results

From the first scatterplot, we found that a linear relationship existed between the percent of those who believe global warming is happening and those who prioritize their candidate's views on global warming. We also found it interesting how there was a clear divide between those who voted Republican vs Democratic in the 2016 presidential election. The correlation coefficient was 0.925, implying that a strong linear relationship existed between those two variables. 

![Image of first scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/scatterplot_CC_Political_Affiliation.png)

From the boxplots, we observed that the average portion of respondents who think global warming is happening and who prioritize candidate’s views on global warming was highest for Democratic counties, as compared to Republican and swing counties. 

![Image of first boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/boxplot1.png) 

![Image of second boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/boxplot2.png) 

From the second scatterplot, we found that a linear relationship existed between the percent of those who believe global warming is happening and those who are worried. It was also evident that population density increased as those variables increased. The correlation coefficient between those who think it is happening and those who are worried was 0.95, implying there was a strong linear relationship. The correlation coefficient between population density and those who are worried was 0.3. This is considered a weak relationship but it does not mean that no relationship exists and may still add value to a model that contains other predictors. 

![Image of second scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/scatterplot_CC_PopDensity.png) 

### First Model Results
Below you can see the residual plots before and after the log transformation, showing that the assumptions for residuals having constant variance and mean 0 were met after the transformation. 

**Before transformation**

![Image of first plot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/residplot_beforeTrans.png) 

**After transformation**

![Image of second plot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/residplot_afterTrans.png) 

As noted above in the experimental design, the assumptions for normality and independence were also met. Our p-value for our model’s F statistic was less than alpha=0.05, indicating that the data supported the claim that a linear relationship exists between those who prioritize candidate's view on GW and those who think GW is happening when also comparing the results from the 2016 presidential election. The t-statistic for each predictor variable had a p-value less than alpha=0.05, indicating that each of our variables added value to the model. Our adjusted R squared for the final model was 86.6%, indicating that about 87% of the variability in the percentage of respondents who prioritize candidate's views on global warming can be explained by the model. 

Interpretation of the coefficient for the Republican indicator variable (-0.0342):

```(exp(-.0342) – 1) * 100 = -3.4```

The percentage of those who prioritize candidate's views on global warming decreases on average by about 3.4% per change in the percentage of those who think GW is happening if they voted Republican in the 2016 election relative to if they voted Democrat. 

### Second Model Results

As noted in the experimental design, the assumptions for a linear regression model were met. The p-value for the F statistic was less than alpha=0.05, indicating that the data supported the claim that a linear relationship exists. The t statistic for each predictor variable was significant (p-value less than alpha=0.05), indicating that each variable added value to the model. Since both predictor variables were continuous, we obtained the VIF to ensure there was no sign of multicollinearity. The VIF values were below 10, indicating no sign of multicollinearity. Our adjusted R-squared for the model was 0.903, indicating that 90.3% of the variability in the percentage of those who are worried about global warming can be explained by the regression model. 

Interpretation of the population density coefficient (.0002):

.0002% is the expected change in the percentage of those who are worried per unit change in the population per sq mi (population density) when the percentage of those who think global warming is happening is held constant.



