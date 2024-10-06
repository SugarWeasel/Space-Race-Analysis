#!/usr/bin/env python
# coding: utf-8

# # Introduction

# <center><img src="https://i.imgur.com/9hLRsjZ.jpg" height=400></center>
# 
# This dataset was scraped from [nextspaceflight.com](https://nextspaceflight.com/launches/past/?page=1) and includes all the space missions since the beginning of Space Race between the USA and the Soviet Union in 1957!

# ### Install Package with Country Codes

# %pip install iso3166

# ### Import Statements

# In[489]:


import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta
from dateutil import parser


# ### Notebook Presentation

# In[490]:


pd.options.display.float_format = '{:,.2f}'.format


# ### Load the Data

# In[491]:


df_data = pd.read_csv("mission_launches.csv")


# # Preliminary Data Exploration
# 
# * What is the shape of `df_data`? 
# * How many rows and columns does it have?
# * What are the column names?
# * Are there any NaN values or duplicates?

# In[492]:


df_data.shape


# <p>The dataframe has 9 columns, with 4324 rows of data.</p>

# In[493]:


df_data.info()


# <p>Above we see the column names, it appears that unamed:0.1 and unamed:0 are columns with the row number.</p>

# ## Checking for duplicates and NaN values ##

# In[494]:


#checking for NaN values
df_data.isna().values.any()


# In[495]:


print(f"There are {df_data.isna().values.sum()} missing values in the dataframe.")


# In[496]:


df_data.isna().sum()


# In[497]:


#checking for duplicate values
df_data.duplicated().values.any()


# <p>The dataset contains no duplicate entries, but does contain Nan values</p>

# In[498]:


#dropping the Nan values and using a separate Dataframe in case cost comparisons need to be made.
df_data_clean = df_data.dropna()
df_data_clean.isna().values.any()


# In[499]:


df_data_clean.info()


# # Number of Launches per Company
# 
# Creating a chart that shows the number of space mission launches by organisation.

# In[500]:


launches_by_org = df_data.Organisation.value_counts()
launches_by_org


# In[501]:


launches = px.bar(launches_by_org, 
                  x = launches_by_org.index, 
                  y = launches_by_org.values,
                  title = 'Space Launches by Organisation',
                 color = launches_by_org.values,
                 color_continuous_scale = 'sunset')

launches.update_layout(yaxis_title = "Number of Launches", coloraxis_showscale = False)

launches.show()


# <p> The former Soviet Union was responsible for the most amount of rocket launches.</p>

# # Number of Active versus Retired Rockets
# 
# How many rockets are active compared to those that are decomissioned? 

# In[502]:


status = df_data.Rocket_Status.value_counts()
status


# In[503]:


# We will do a bar char to visualize this, but first let's provide a list of values for the x axis (x = ["Yes", "No"]) instead of using the index

rocket_status = px.bar(
    status,
    x=['Active', 'Retired'],
    y = status.values,
    color = status.values
)
rocket_status.update_layout(title = 'Active vs Decommissioned Rockets', yaxis_title = "Number of Rockets", coloraxis_showscale = False, yaxis_range =[0,4000])

rocket_status.show()
    


# # Distribution of Mission Status
# 
# How many missions were successful?
# How many missions failed?

# In[504]:


df_data.Mission_Status.value_counts()


# <p>Here we see 3879 missions were successful, and 445 experience failure of some type.</p>

# # How Expensive are the Launches? 
# 
# Create a histogram and visualise the distribution. The price column is given in USD millions (careful of missing values). 

# In[505]:


# the histogram will be sorted by price in ascending order

price_hist = px.histogram(df_data_clean, x='Price', histnorm = 'percent', nbins = 30, opacity = 0.9, title ="Space Mission Cost Histogram").update_xaxes(categoryorder='total ascending')

price_hist.update_layout(xaxis_title = "Cost of Mission in $ Millions")


# <p>From the analysis, the majority of space launches are 450+ million at 14.0%. This price also marks the highest cost for space missions.</p>

# # Use a Choropleth Map to Show the Number of Launches by Country
# 
# * Create a choropleth map using [the plotly documentation](https://plotly.com/python/choropleth-maps/)
# * Experiment with [plotly's available colours](https://plotly.com/python/builtin-colorscales/). I quite like the sequential colour `matter` on this map. 
# * You'll need to extract a `country` feature as well as change the country names that no longer exist.
# 
# Wrangle the Country Names
# 
# You'll need to use a 3 letter country code for each country. You might have to change some country names.
# 
# * Russia is the Russian Federation
# * New Mexico should be USA
# * Yellow Sea refers to China
# * Shahrud Missile Test Site should be Iran
# * Pacific Missile Range Facility should be USA
# * Barents Sea should be Russian Federation
# * Gran Canaria should be USA
# 
# 
# You can use the iso3166 package to convert the country names to Alpha3 format.

# In[506]:


df_data.Location.value_counts()


# <p>Russia, Barents Sea, Sharud, Pacific Missile Range, North Korea, Gran Canaria need to be converted. </p>

# <h3>Changing some locations to country names.</h3>

# In[507]:


# Use manual mapping

location_dict = {
    'Yellow Sea' :'China',
    'Barents Sea' : 'Russian Federation',
    'Shahrud Missile Test Site' :'Iran, Islamic Republic of',
    'North Korea': 'Korea, Democratic People\'s Republic of',
    'Pacific Missile Range Facility': 'USA',
    'Gran Canaria' :'USA',
    'Russia': 'Russian Federation'
}


# <h3>Converting string to ISO</h3>

# In[508]:


# Can be done by splitting the each location by comma and getting that data. For example:
country_name = df_data.Location[200].split(",")[-1].strip()   #.strip to remove any extra whitespaces
print(country_name)
countries.get(country_name).alpha3    # alpha three returns 3 letter iso


# In[509]:


#Putting this into a function

def get_iso(location):
    try:

        # loop through each dict key/value
        for key, country in location_dict.items():
            #if key is present anywhere in location string
            if key in location:
                #access the value of the key and get the 3 letter ISO code
                return countries.get(country).alpha3
                
         # if manual mapping doesn't work...       
        country_name = location.split(",")[-1].strip()
        return countries.get(country_name).alpha3

    except KeyError:
        return None
df_data['ISO'] = df_data['Location'].apply(get_iso)


# In[510]:


# making a new dataframe with the counts
launches_by_country = df_data.ISO.value_counts().reset_index()

launches_by_country


# In[511]:


map = px.choropleth(launches_by_country, 
                    locations = 'ISO', 
                    color = 'ISO',
                    color_continuous_scale = 'solar',
                   hover_name ='ISO',
                   hover_data ={'count':True})
map.show()


# In[ ]:





# In[ ]:





# # Use a Choropleth Map to Show the Number of Failures by Country
# 

# In[512]:


df_data.head()


# In[513]:


df_data.loc[df_data['Mission_Status'] != 'Success'].tail(30)


# In[514]:


# first we need to group all failure types together: this code handles it by creating a new dataframe to include only failures
# df_data.loc[df_data['Mission_Status'] != 'Success']

# then we can groupby
failures = df_data.loc[df_data['Mission_Status'] != 'Success'].groupby(['ISO'], as_index = False).agg({'Mission_Status':pd.Series.count})


# In[515]:


# renaming the columns
failures.rename(columns={'Mission_Status':'Failures'}, inplace= True)


# In[516]:


map = px.choropleth(failures, 
                    locations = 'ISO', 
                    color = 'ISO',
                    color_continuous_scale = 'solar',
                   hover_name ='ISO',
                   hover_data ={'Failures':True})
map.show()


# In[ ]:





# # Create a Plotly Sunburst Chart of the countries, organisations, and mission status. 

# In[517]:


df_data


# In[518]:


# Creating a dataframe that groups by country, org, and mission status, then count occurences of each combination.
iso_status = df_data.groupby(['ISO', 'Organisation', 'Mission_Status']).size().reset_index(name='counts')
iso_status


# In[519]:


# Define a custom color mapping for different Mission_Status values

color_mapping = {
    'Success' :'green',
    'Partial Failure' :'Yellow',
    'Failure': 'red',
}


sunburst = px.sunburst(iso_status,
                       path=['ISO', 'Organisation', 'Mission_Status'],  # define hierarchy
                       values = 'counts',
                       color = 'Mission_Status',
                       color_discrete_map = color_mapping,
                       title= 'Sunburst Launch Chart by Country, Organisation, and Mission Result')
sunburst.show()


# In[ ]:





# # Analyse the Total Amount of Money Spent by Organisation on Space Missions

# In[520]:


# we'll use the clean df with the no cost values dropped for a accurate analysis
# however, we'll need to convert the dtype to an int64 in order to sum up price


# In[521]:


df_data_clean.info()


# <h2> The Price must be converted to a int or float</h2>

# In[522]:


# first we'll remove all the commas then convert to float
df_data_clean['Price'] = df_data_clean['Price'].str.replace(',','').astype(float)




# In[523]:


df_data_clean.info()


# In[524]:


money_spent_per_org = df_data_clean.groupby(['Organisation'], as_index = False).agg({'Price': pd.Series.sum})
money_spent_per_org


# In[525]:


money_bar = px.bar(
    money_spent_per_org,
    x='Organisation',
    y='Price',
    color = 'Price',
    color_continuous_scale = 'sunset',
    title='Money spent per organisation'
)

money_bar.update_layout(yaxis_title = 'Price in $ Millions',
                       coloraxis_showscale = False)

# change to y axis to log scale
money_bar.update_yaxes(type = 'log')


# # Analyse the Amount of Money Spent by Organisation per Launch

# In[526]:


# here we will average the prices to determine a per launch value
org_avg_spend = df_data_clean.groupby(['Organisation'], as_index = False).agg({'Price': pd.Series.mean})


# In[527]:


money_bar = px.bar(
    org_avg_spend,
    x='Organisation',
    y='Price',
    color = 'Price',
    color_continuous_scale = 'sunset',
    title='Average Cost per Launch'
)

money_bar.update_layout(yaxis_title = 'Price in $ Millions',
                       coloraxis_showscale = False)

# change to y axis to log scale
money_bar.update_yaxes(type = 'log')


# In[528]:


df_data.loc[13]


# # Chart the Number of Launches per Year

# In[529]:


df_data.Date[105]


# In[530]:


pd.to_datetime(df_data.Date[105], format = "%a %b %d, %Y %H:%M %Z")


# In[531]:


df_data.Date[106]


# In[532]:


pd.to_datetime(df_data.Date[106], format = "%a %b %d, %Y")


# <p>As shown above, we have two different formats shown across the rows, some dates have a time, while some don't. Passing this through the to_datime method will usually throw an error since the formats are not consistent.</p>

# In[533]:


# making a function to handle different formats. We will convert all times to UTC

def date_process (x):
    only_date_format = "%a %b %d, %Y"
    
    try:
        return pd.to_datetime(x, utc = True)

    # For values with date-only, we will handle this exception.
    except ValueError:
        return pd.to_datetime(x, format = only_date_format, utc = True)


# In[534]:


df_data['Date'] = df_data['Date'].apply(date_process)


# <h3>Repeating process for clean DF</h3>

# In[535]:


df_data_clean['Date'] = df_data_clean['Date'].apply(date_process)


# <h3>Checking our work</h3>

# In[536]:


df_data.info()


# In[537]:


df_data_clean.info()


# <h3>Adding columns for year and months</h3>

# In[538]:


# this will be done by adding a column with the year of launch

# first creating a datetime index from the release date column
dates = pd.DatetimeIndex(data=df_data.Date)
years = dates.year
months = dates.month


df_data.insert(5, 'Year', years)
df_data.insert(6, 'Month', months)


# In[539]:


df_data.head()


# <h2>Finally, we can start plotting our graph.</h2>

# In[540]:


# let's group the launches by year first
launches_per_year = df_data.Year.value_counts()



# In[541]:


year_launches = px.bar(launches_per_year,
                       x=launches_per_year.index,
                       y = launches_per_year.values,
                       color = launches_per_year.values,
                       color_continuous_scale = 'dense'
                      )
year_launches.update_layout(title = 'Launches per Year', yaxis_title = 'Number of Launches', xaxis_title = 'Year')

year_launches.show()
                       
                       
                       


# <p>2018 has the most launches since 1957</p>

# # Chart the Number of Launches Month-on-Month until the Present
# 
# Which month has seen the highest number of launches in all time? Superimpose a rolling average on the month on month time series chart. 

# In[542]:


launches_ordered = df_data.sort_values(by='Date')
# group by year and month, use size to get number of elements and reset index
launch_counts = launches_ordered.groupby(['Year','Month']).size().reset_index(name = 'Launches')
launch_counts


# In[543]:


# Create a new datetime column to represent Year-Month for plotting
launch_counts['Date'] = pd.to_datetime(launch_counts['Year'].astype(str) + '-' + launch_counts['Month'].astype(str))
launch_counts


# <h4>Specifying a moving avg</h4>

# In[544]:


# we'll take 4 observations and average them
launch_counts['Roll_avg_launches']= launch_counts.Launches.rolling(window = 4).mean()
launch_counts


# In[550]:


year_launches = px.line(launch_counts,
                       x='Date',
                       y = 'Launches',
                        width = 1500, height = 720
                       
                      )
year_launches.update_layout(title = 'Launches over time', yaxis_title = 'Number of Launches', xaxis_title = 'Date')

year_launches.add_scatter(x=launch_counts.Date, y=launch_counts.Roll_avg_launches, mode='lines', name='4-Month Rolling Avg', line=dict(color='red'))


year_launches.show()
                       


# <h4>As we can see, December of 1971 was the most popular month of all time for space launches.</h4>

# # Launches per Month: Which months are most popular and least popular for launches?
# 
# Some months have better weather than others. Which time of year seems to be best for space missions?

# In[552]:


month_popularity = df_data.Month.value_counts()
month_popularity


# In[555]:


month_bar = px.bar(month_popularity,
                   x=month_popularity.index,
                   y=month_popularity.values,
                   color = month_popularity.values,
                   color_continuous_scale='agsunset',
                   title = 'Total launches per Month'
                  )
month_bar.update_layout(xaxis_title = 'Month', yaxis_title ='Number of Launches during Month')

month_bar.show()


# <p>Based on the chart, December is the most popular month for space launches.</p>

# # How has the Launch Price varied Over Time? 
# 
# Create a line chart that shows the average price of rocket launches over time. 

# In[560]:


#First sort the data by date, and use the clean_df which has no cost missions removed.
sorted_price = df_data_clean.sort_values('Date')


# In[574]:


cost_line = px.scatter(sorted_price,
                    x='Date',
                    y='Price',
                    title = 'Cost of Space Missions over Time',
                    color = 'Price',
                    color_continuous_scale = 'mygbm',
                    
)

cost_line.update_layout (xaxis_title = 'Date',
                         yaxis_title = 'Cost in $ Millions',
                        template = 'ggplot2',
                        xaxis_range = ['1963-01-01', '2021-12-31'],  # Set x-axis limits]
)

# change to y axis to log scale
cost_line.update_yaxes(type = 'log')

cost_line.show()


                    


# <p>From the scatter plot. The range in prices has increased. Within the past 15 years, cheap space flights have increased in popularity ($<60 million)</p>

# # Chart the Number of Launches over Time by the Top 10 Organisations. 
# 
# How has the dominance of launches changed over time between the different players? 

# In[ ]:





# In[ ]:





# In[ ]:





# # Cold War Space Race: USA vs USSR
# 
# The cold war lasted from the start of the dataset up until 1991. 

# In[ ]:





# In[ ]:





# ## Create a Plotly Pie Chart comparing the total number of launches of the USSR and the USA
# 
# Hint: Remember to include former Soviet Republics like Kazakhstan when analysing the total number of launches. 

# In[ ]:





# In[ ]:





# ## Create a Chart that Shows the Total Number of Launches Year-On-Year by the Two Superpowers

# In[ ]:





# In[ ]:





# ## Chart the Total Number of Mission Failures Year on Year.

# In[ ]:





# In[ ]:





# ## Chart the Percentage of Failures over Time
# 
# Did failures go up or down over time? Did the countries get better at minimising risk and improving their chances of success over time? 

# In[ ]:





# In[ ]:





# In[ ]:





# # For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including including 2020)
# 
# Do the results change if we only look at the number of successful launches? 

# In[ ]:





# In[ ]:





# # Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches
# 
# Which organisation was dominant in the 1970s and 1980s? Which organisation was dominant in 2018, 2019 and 2020? 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




