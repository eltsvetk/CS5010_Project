# Intro and Data:
## (SLIDE: Title and pictures of the 3 of us)
*Jonathan:* Hello, our group set out to look at Americans’ attitudes toward Climate Change – specifically, whether those attitudes correlate with Population Density.  Our group members are Elena Tsvetkova, Anita Taucher, and I’m Jonathan Shakes.

## SLIDE: YALE WEBSITE
*Jonathan:* Some of our data comes from the Yale Program on Climate Change Communications. They ask survey questions like, “Do you think climate change is happening,” or “Do you think your state governor should be doing more about climate change?” 

On top of the Yale data, we add census data about population density, to see if that’s a predictor of people’s climate change attitudes.

We also added election return data from the 2016 presidential race between Donald Trump and Hillary Clinton. I guess the Yale program folks want to downplay the politics, because they don’t publish their data with a political overlay. Their FAQ did say population density would be an interesting angle they had not followed.

## SLIDE: Side-by-side rows from two different data sets
*Jonathan:* Before we could do any analysis, we had to merge the data at the county level. You’d think that would be easy, right? There used to be a standard code for counties called a FIPS code, but in 2008 the commerce department replaced with another standard called INCITS, and our sources were inconsistent. It’s not practical to manually check that 3000 counties match correctly.   So we wrote python functions that translate each coding standard into the one we used, then used that as an index to combine datasets.

# MAP
An interactive map allows those curious about climate change to compare the attitudes of Americans across the country, in a single visualization.

It is available at https://climate-population.herokuapp.com/

The choropleth map is built using Plotly, rendered as a Dash application, and deployed on Heroku for all to access.

The map expedites choosing a survey data point the user is interested in, and immediately renders a comparison of American's attitudes across the country, at the county level.  It also allows users to assess the current state of the country's thoughts about each data point.

Hovering over a location on the map provides: 
*	The County name and State
*	The percentage of county residents that agree with the selected data point.
*	The *population density* of that county
*	The number of votes for Democrats and Republicans in the 2016 election.  

The selectable data points to _6 items_, in order to reduce the initial map loading time, which stands at about 1 minute.


# ANALYSIS
## SLIDE: Scatterplots and models w/ interpretations

*Elena:* Our first question was: Do those who think GW is happening also think the candidate’s views on GW is important? And how does this relate to the 2016 presidential election?

From the scatterplot, you can see there is a linear relationship between those who believe GW is happening and those who prioritize candidate's views on GW. It is also interesting how there is a clear divide between those who voted democrat vs republican in the 2016 election.  

![Image of first scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/scatterplot_CC_Political_Affiliation.png)

Notice these boxplots. You can see that the average % of those who think GW is happening and those who prioritize candidate’s views on GW is highest for democratic counties.

![Image of first boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/boxplot1.png)

![Image of second boxplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/boxplot2.png)

But we wanted to dive deeper. We wanted to understand the relationship between these variables. So, I utilized the statsmodels library in python. I fit a model where 87% of the variability in those who prioritize candidate’s views on GW was captured. I did have to log transform the response to ensure the assumptions for a multiple regression model were met. In the end, I found that those who prioritize candidate’s views on GW decreases on average by about 3.8% per change in those who think GW is happening if they voted Republican in the 2016 election instead of voting Democrat. 

Our second question was: Are the people who think GW is happening actually worried about it and how does this relate to population density?

Notice how there is a linear relationship between those who believe GW is happening and those who are worried. Notice how the population density increases as those who think GW is happening and are worried increases. I fit another model where 90% of the variability in those who are worried about GW was captured. We found that .0002% is the expect change in those who are worried per unit change in the population density when those who believe GW is happening is held constant. 

![Image of second scatterplot](https://raw.githubusercontent.com/eltsvetk/CS5010_Project/main/scatterplot_CC_PopDensity.png)

# TESTING (60 words)

# CONCLUSION (100 words)
*Jonathan:* Our hypothesis was that climate-change-related attitudes in dense cities will be significantly different than those in rural areas. 
This is an important question because humans are migrating towards cities, and if people in cities “lose touch” with the importance of protecting the environment, that could impact the political will to protect the environmental, especially in a democracy.
This would be a place for 
> Inspirational Quote
> That leaves people with
> Tears in their eyes
