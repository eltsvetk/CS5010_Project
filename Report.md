# U.S. Climate Change Attitudes

Term Project for CS5010, Spring 2021

Group 4: Elena Tsvetkova (rrm3nh@),  Anita Taucher (agt4vw@), and Jonathan Shakes (hqe7rd@)

## INTRODUCTION
We set out to answer a hypothesis: climate-change-related attitudes in cities will be significantly different than those in rural areas. This topic area is interesting, because around the world, humans are migrating towards cities. If people in cities “lose touch” with the importance of protecting the environment, that would have implications for environmental health, especially in a democracy like the U.S., where voters ultimately decide whether to enact and enforce laws that limit destruction of the natural world. Without such legal protection, the environment suffers due to what economists call "negative externalities" and the "tragedy of the commons." 

To study this topic, we needed public-opinion data about environmental data, with a distinction between people living in city and rural areas.

## THE DATA
Prior to beginning studies at UVA, Jonathan learned about climate-change-related survey data during volunteer work he did with Citizens’ Climate Lobby (CCL)<sup>[1](#Note1)</sup>. Anita and Elena shared Jonathan’s interest in the general topic. CCL uses the survey data as part of its grass-roots mobilization within the US. Understanding what voters believe about climate change policy is an important piece of data to inform effective grass-roots advocacy.

Our core data set comes from the Yale Program on Climate Change Communications<sup>[2](#Note2)</sup> <sup>[3](#Note3)</sup>. The Yale data contains multi-year results from surveys in the U.S.. Our data file from Yale consists of about 5000 rows, each corresponding to a geographic area, and several dozen columns with responses to questions like, “Do you think climate change is happening,” or “Do you think your state's governor should do more about climate change?”  These surveys were administered from 2018 to 2020. The sample size is large enough to support results broken out at the level of U.S. counties and congressional districts, opening the possibility for us to do map-based geographic analysis.

We decided that looking at the data through the lens of the urban/rural divide, using population density as a numeric indicator, might add value to this existing data set.  In an FAQ for the dataset, we discovered that the data’s relation with population density is both of general interest and not something that has been done before<sup>[4](#Note4)</sup>.  The potential to look at less-traveled territory made our project more interesting to us, even though we’re realistic enough to understand that our class project is unlikely to break serious new ground, from an academic perspective.

The survey data was limited to the US. While the climate change problem is a global one,  the data was so valuable and relevant that we decided to center our work on it.

At the finest level of detail, the Yale data is split by county and congressional district.  We chose to focus on county, not congressional district, because there are nearly six times as many counties as congressional districts, and therefore our maps might show finer gradations in degree as population density drops in correlation with the distance from the densest cities.

The population and land-area at the county-level were each obtained in separate files from the US Census Bureau<sup>[5](#Note5)</sup> <sup>[6](#Note6)</sup>.  By matching these two files together, dividing population by land area, we calculated the population density per square mile of land for each county or county-equivalent geographic portion of the U.S.. 

We also assembled the 2016 presidential election returns for each county in the US from the Election Lab at MIT<sup>[7](#Note7)</sup>. By looking at the vote totals in each county, we could categorize each county as Republican or Democratic. That was an important step for our study, because political preferences are commonly known to be linked to climate change attitudes. Political data was not included in the Yale dataset, but it helped us determine whether population density had any significant correlation with climate-change attitudes, beyond what political preferences alone would predict.

Finally we scraped yet another web data source, Ballotpedia, to identify a list of 206 “swing counties” in the US where a majority of voters voted for Obama in 2008 and 2012, then swung Republican in 2016, voting for Donald Trump<sup>[8](#Note8)</sup>.  The entire list of swing counties was visible on a single web page, so scraping was a simple matter of identifying the correct chunk of HTML and then removing the extraneous tags and data.  Note: This portion of our work went beyond the basic requirements of the project.

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

## Mapping
Based on the statistical analysis, we anticipated that an interactive map of the country, built on the county-level data would be an effective way to communicate results to our audience.

Using plotly, we built a choropleth from county-level geojson data, imported from plotly’s github content repository.  We experimented with map features, such as using colors and the hover box to convey the story, and quickly came to the decision that we wanted the users to choose map content from a list of possibilities that support the climate change questions that we investigated in this project. This would also require users to have the ability to access the map on the web, as opposed to downloading code to their local machine.

As a result, we chose a combination of survey and political data to drive the map content.

![Image of Map with List](https://github.com/eltsvetk/CS5010_Project/raw/main/interactive-map/MapShowingExpandedList.png)

In the hover box, which is one of the core implements for comparing data across the map, we decided to show similar values for all counties, in addition to the value selected by the user.  In the example below, the user has selected “This is happening”, which is displayed on the right.  On the left, the user can see the items we felt were key to the drawing conclusions on the hypothesis:  County Name, Population Density, and Political information.

![Image of Map Hover Box](https://github.com/eltsvetk/CS5010_Project/raw/main/interactive-map/MapHoverBox.png)

We implemented the map as a Dash application, deployed on heroku, for general web access:  

https://climate-population.herokuapp.com

Heroku provides limited resources for free.  We found that implementing about 6 items, driving 6 different content maps, takes about 1 minute to load.  We considered 1 minute to be our maximum threshold for waiting on a result.  In the code, we reduced the number of columns in the dataset, so that we were working with only the specific data we needed, in order to save resources.

## TESTING
For the Python coding portion of this project, we wrote scripts to 

* Convert a specific set of data files into a merged data file,
* Perform statistical analysis on the merged data, and
* Create relevant maps and charts.

The scripts had a few helper functions, but nothing with complex logic that would benefit from the object-oriented features of Python. Since the scripts are for one-time use, rather than being designed to handle a wide variety of unpredictable scenarios, formal specification and unit testing seemed not applicable, as long as the data we generated itself was accurate.

As a result, our "testing" script was focused on the data itself (Note 9).  As we transformed and merged the data sets, we used tests to confirm, for example, that

* The total population in our main merged data frame roughly matches the population of the United States
* The total land area roughly matches
* The number of voters for Clinton and Trump in 2016 aligns with an independent source for this aggregate data
* We didn’t have duplicate data in columns where duplicates were not expected.

We also tested each other’s code by reviewing it and confirming that we understood it and that it works as intended. 

## CONCLUSION - WHAT WE LEARNED ABOUT THE DATA
The following bar graph summarizes a key finding of our project. It's commonly known that cities tend to vote Democratic, and Democrats express more environmental concern at the voting booth than Republicans, so it's no surprise to see that climate change attitudes differ along party lines.

What's more interesting is that regardless of whether a county votes Democratic or Republican, people in counties with higher population density express more concern about climate change. 

![Image of Concluding Barplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/statistical_analysis/images/BarGraphWithDensityEffect.png) 

Before we started the project, we wondered if migration will mean people in cities forget what they left behind, and not care about environmental destruction. This graph suggests an opposite hypothesis: people currently in the cities care more about protecting the environment than people in the countryside.

Before we can say there is no cause for worry, additional work is needed to explore whether a causal relationship exists.  To do that, we would need to look at people’s attitudes over time, or find a way to measure the recency of people’s transition into an urban environment.  We would also control for other variables that we haven’t yet controlled for, for example income, education, and depth of party loyalty in each county.

It’s also worth examining why the gap between low-density and high-density counties for each response category is so predictably consistent.  
From the map we learned, when choosing the list items, consecutively from first to third:  

1. People generally agree that Climate Change is happening.  The map is a brighter yellow color to indicate the agreement.
2. People are somewhat worried about Climate Change.  The map is a little bit darker than the first selection, indicating that people do not agree as strongly that they are worried.
3. Voting Priority shows a generally darkened map.  This indicates that people are generally not voting for candidates based on this particular issue.

The progression of the map from lighter to darker on these items, that even if people agree it is happening, and even though some are concerned, people are generally not voting for political candidates based on Climate Change.

## CONCLUSION - WHAT WE LEARNED ABOUT DATA SCIENCE
In addition to learning a bit about climate change attitudes in the U.S., the three of us accomplished several first-ever’s for this project.  It was our first time to...

* Write scripts to clean and merge real-world data from disparate sources
* Use Python for statistical analysis and predictive modeling 
* Use geojson data to build a choropleth map
* Use Dash to create a web application
* Use Heroku to deploy an interactive map as part of a website
* Use Python for something beyond a class assignment
* Use GitHub commands such as pull, commit, add and push, for truly managing code being updated by multiple people

## BEYOND THE ORIGINAL SPECIFICATIONS
To summarize what are team did beyond the original specifications

1. Web-scraped swing county data
2. Built statistical models along with transformed response variable to improve predictive ability of one of our statistical models
3. Built interactive map that was incorporated into a website

## FOOTNOTES

<a name="Note1">Note 1</a>: CCL is a non-partisan, volunteer-driven organization that works to ensure our planet remains livable through the adoption of fair, effective, and sustainable climate change solutions.

<a name="Note2">Note 2</a>:  https://climatecommunication.yale.edu/

<a name="Note3">Note 3</a>: Howe, P., Mildenberger, M., Marlon, J., & Leiserowitz, A. (2015) “Geographic variation in opinions on climate change at state and local scales in the USA,” Nature Climate Change. DOI: 10.1038/nclimate2583.

<a name="Note4">Note 4</a>: https://climatecommunication.yale.edu/visualizations-data/ycom-us/

<a name="Note5">Note 5</a>: US Census, Annual Estimates of the Resident Population for Counties: April 1, 2010 to July 1, 2019

<a name="Note6">Note 6</a>: https://www.census.gov/library/publications/2011/compendia/usa-counties-2011.html#LND

<a name="Note7">Note 7</a>: https://electionlab.mit.edu/data

<a name="Note8">Note 8</a>: https://ballotpedia.org/Pivot_Counties_by_state






