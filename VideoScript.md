# Intro and Data:
## SLIDE: Title 
*Jonathan:* Hello, our group looked at Americans’ attitudes toward Climate Change – specifically, whether those attitudes correlate with Population Density.  Our group members are Elena TsvetKOHva, Anita Taucher, and I’m Jonathan Shakes.

## SLIDE: YALE WEBSITE
*Jonathan:* Some of our data comes from the Yale Program on Climate Change Communications. The Yale program does surveys with questions like, “Do you think climate change is happening,” or “Do you think your state's governor should do more about climate change?” 

On top of the Yale data...

## SLIDE: MULTIPLE DATA SOURCES

...we added census data about population density, to see if that relates to people’s climate change attitudes.

We also add election return data from the 2016 presidential race between Donald Trump and Hillary Clinton. That categorized each county as Republican or Democratic. We scraped another source for a list of Swing counties.  

Before doing analysis, we merged these data sources at the county level. That should be easy, and there used to be a standard ID for counties called a FIPS code, but in 2008 the commerce department replaced that with another standard called INCITS, so our sources were inconsistent.

## SLIDE: County conversion Python code
*Jonathan:* It’s not practical to manually match 3000 counties, so we wrote python functions to translate between coding standards, then used a single coding standard as an index to combine five different data frames, one for each data source.


# ANALYSIS
## SLIDE: Scatterplots and models w/ interpretations

*Elena:* Our first question was: Do those who think GW is happening also think the candidate’s views on GW is important? And how does this relate to the 2016 presidential election?

From the scatterplot, you can see there is a linear relationship between those who believe GW is happening and those who prioritize candidate's views on GW. It is also interesting how there is a clear divide between those who voted democrat vs republican in the 2016 election.  

![Image of first scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/scatterplot_CC_Political_Affiliation.png)

Notice these boxplots. You can see that the average % of those who think GW is happening and those who prioritize candidate’s views on GW is highest for democratic counties.

![Image of first boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/boxplot1.png)

![Image of second boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/boxplot2.png)

But we wanted to dive deeper. We wanted to understand the relationship between these variables. So, I utilized the statsmodels library in python. I fit a model where 87% of the variability in those who prioritize candidate’s views on GW was captured. I did have to log transform the response to ensure the assumptions for a multiple regression model were met. In the end, I found that those who prioritize candidate’s views on GW decreases on average by about 3.4% per change in those who think GW is happening if they voted Republican in the 2016 election instead of voting Democrat. 

Our second question was: Are the people who think GW is happening actually worried about it and how does this relate to population density?

Notice how there is a linear relationship between those who believe GW is happening and those who are worried. Notice how the population density increases as those who think GW is happening and are worried increases. I fit another model where 90% of the variability in those who are worried about GW was captured. We found that .0002% is the expect change in those who are worried per unit change in the population density when those who believe GW is happening is held constant. 

![Image of second scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/scatterplot_CC_PopDensity.png)

# MAP
## SLIDE: About the interactive Choropleth map

*Anita:* We anticipated that an interactive map, built on the county-level data we collected would be an effective way for users to consume the amount of information we needed to convey, and it would provide an effective opportunity to compare the survey data with political insights across the country.  

So, based on the statistical analysis, we decided on the most impactive data points, and created an interactive choropleth map that allows users to choose survey data and political affiliations in a single experience.

It is available at https://climate-population.herokuapp.com/.  It takes about a minute or so to load, but once it is loaded, the interaction exhibits no lag.

The choropleth map is built using Plotly Graph Objects, rendered as a Dash application, and deployed on Heroku for all to access.  We use a continuous development environment, where any change to the Github code immediately rebuilds and redeploys the application.

## SLIDE: Picture of the map

*Anita:* The map expedites choosing a survey data point the user is interested in, and immediately renders a comparison of American's attitudes across the country, at the county level.  It also allows users to assess the current state of the country's thoughts about each data point.

Hovering over a location on the map provides: 
*	The County name and State
*	The percentage of county residents that agree with the selected data point.
*	The *population density* of that county
*	The number of votes for Democrats and Republicans in the 2016 election.  

We implemented 5 selectable data points, in order to focus our story, and reduce the initial map loading time, which stands at about 1 minute.



# TESTING 
*Jonathan:* The code for our project is in three scripts. One script loads and cleans the data, a second script does the statistical analysis and data plots, and a third script does the interactive mapping. Most of our testing was whitebox testing, meaning we looked at each other's code, to make sure we understood it. 

# CONCLUSION SLIDE 1
*Jonathan:* This bar graph summarizes a key finding of our project. It's commonly known that cities tend to vote Democratic, and Democrats express more environmental concern than Repubicans, so it's no surprise to see that climate change attitudes differ along party lines.

# CONCLUSION SLIDE 2

What's more interesting is that regardless of whether a county votes Democratic or Republican, people in counties with higher population density express more concern about climate change. The light red and light blue bars are for sparsely populated counties, and you can see the concern gets bigger with the dark red and dark blue bars, which are for dense urban counties.
 
This is important because all over the world, people are migrating into cities, and in a city, it's harder to stay in touch with the natural environment. It's possible that migration will mean people in cities forget what they left behind, and not care about environmental destruction.  We would need to do more work to explore a causal relationship, but this graph suggests an opposite hypothesis: people currently in the cities care *more* about protecting the environment than people in the countryside. 

That's great news for a democracy where more are more people will live in cities. City dwellers who want to protect the environment will increase the odds that our country takes action to address climate change.

# EXTRA CREDIT SLIDE

That concludes our presentation, and MOST of our audience does NOT need to read this slide.




