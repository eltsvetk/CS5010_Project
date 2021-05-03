# Intro and Data:
## (SLIDE: Title and pictures of the 3 of us)
*Jonathan:* Hello, our group looks at Americans’ attitudes toward Climate Change – specifically, whether those attitudes correlate with Population Density.  Our group members are Elena Tsvetkova, Anita Taucher, and I’m Jonathan Shakes.

## SLIDE: YALE WEBSITE
*Jonathan:* Some of our data comes from the Yale Program on Climate Change Communications. The Yale program does surveys with questions like, “Do you think climate change is happening,” or “Do you think your state's governor should do more about climate change?” 

On top of the Yale data, we add census data about population density, to see if that’s a predictor of people’s climate change attitudes.

We also add election return data from the 2016 presidential race between Donald Trump and Hillary Clinton. I think the Yale program folks want to downplay the politics, because they don’t integrate political data with their climate survey data, even though they are closely linked. 

## SLIDE: Side-by-side rows from two different data sets
*Jonathan:* Before doing analysis, we merge the data at the county level. That should be easy, and there used to be a standard ID for counties called a FIPS code, but in 2008 the commerce department replaced that with another standard called INCITS, so our sources were inconsistent. It’s not practical to manually match 3000 counties, do we wrote python functions to translate between coding standardd, then used one version as an index to combine datasets.


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
## SLIDE: Picture of the map

*Anita:* An interactive map allows those curious about climate change to compare the attitudes of Americans across the country, in a single visualization.

It is available at https://climate-population.herokuapp.com/

The choropleth map is built using Plotly, rendered as a Dash application, and deployed on Heroku for all to access.

The map expedites choosing a survey data point the user is interested in, and immediately renders a comparison of American's attitudes across the country, at the county level.  It also allows users to assess the current state of the country's thoughts about each data point.

Hovering over a location on the map provides: 
*	The County name and State
*	The percentage of county residents that agree with the selected data point.
*	The *population density* of that county
*	The number of votes for Democrats and Republicans in the 2016 election.  

The selectable data points to _6 items_, in order to reduce the initial map loading time, which stands at about 1 minute.



# TESTING 
*Jonathan:* We had every intention to practice what we learned in class about unit testing, but that didn't work out, maybe because our data pipeline was a series of three scripts. One script loads and cleans the data, a second script does the statistical analysis and data plots, and a third script does the interactive mapping. The scripts are short, and honestly I think finding ways to make them shorter by using more library functions seems like it will have a bigger impact on quality, as compared to spending the same time to test our own complicated code. 

In any case, we ended up doing something like whitebox testing, meaning we looked at each other's code, to make sure we understood it. 

# CONCLUSION (100 words)
*Jonathan:* In conclusion, look at the biggest circles in this graphic.  Those are the counties with the highest population densities in the country.  It's commonly known that big cities vote Democratic, but this graph shows that big-city residents are also more worried about climate change than residents of typical counties who agree that climate change is happening.
 
This is an important observation, because all over the world, people are migrating towards cities, and when you live in a city, it's harder to stay in touch with the natural environment. It's possible that might mean people in cities will forget what they left behind.  We didn't have time or resources to fully explore that hypothesis, but the good news is that this graph suggests it may actually be the opposite: it seems people in the city care *more* about protecting the environment. In the democracy we live in, that could help build the political will to protect the environment and take action on climate change.

