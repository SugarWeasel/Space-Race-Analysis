#!/usr/bin/env python
# coding: utf-8

# # Introduction

# <center><img src="https://i.imgur.com/9hLRsjZ.jpg" height=400></center>
# 
# This dataset was scraped from [nextspaceflight.com](https://nextspaceflight.com/launches/past/?page=1) and includes all the space missions since the beginning of Space Race between the USA and the Soviet Union in 1957!

# ### Install Package with Country Codes

# %pip install iso3166

# ### Import Statements

# In[25]:


import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta


# ### Notebook Presentation

# In[26]:


pd.options.display.float_format = '{:,.2f}'.format


# ### Load the Data

# In[27]:


df_data = pd.read_csv("mission_launches.csv")


# # Preliminary Data Exploration
# 
# * What is the shape of `df_data`? 
# * How many rows and columns does it have?
# * What are the column names?
# * Are there any NaN values or duplicates?

# In[28]:


df_data.shape


# <p>The dataframe has 9 columns, with 4324 rows of data.</p>

# In[29]:


df_data.info()


# <p>Above we see the column names, it appears that unamed:0.1 and unamed:0 are columns with the row number.</p>

# ## Checking for duplicates and NaN values ##

# In[30]:


#checking for NaN values
df_data.isna().values.any()


# In[31]:


print(f"There are {df_data.isna().values.sum()} missing values in the dataframe.")


# In[32]:


df_data.isna().sum()


# In[39]:


#checking for duplicate values
df_data.duplicated().values.any()


# <p>The dataset contains no duplicate entries, but does contain Nan values</p>

# In[34]:


#dropping the Nan values, inplace parameter so we can overwrite dataframe
df_data.dropna(inplace = True)
df_data.isna().values.any()


# # Number of Launches per Company
# 
# Creating a chart that shows the number of space mission launches by organisation.

# In[52]:


launches_by_org = df_data.Organisation.value_counts()
launches_by_org


# In[61]:


launches = px.bar(launches_by_org, 
                  x = launches_by_org.index, 
                  y = launches_by_org.values,
                  title = 'Space Launches by Organisation',
                 color = launches_by_org.values,
                 color_continuous_scale = 'sunset')

launches.update_layout(yaxis_title = "Number of Launches", coloraxis_showscale = False)

launches.show()


# <p> The CASC (China Aerospace Science and Technology Corporation) is responsible for the highest number of launches. It is a state owned, unlike companies like SpaceX and Northrop.</p>

# # Number of Active versus Retired Rockets
# 
# How many rockets are active compared to those that are decomissioned? 

# In[68]:


status = df_data.Rocket_Status.value_counts()
status


# In[79]:


# We will do a bar char to visualize this, but first let's provide a list of values for the x axis (x = ["Yes", "No"]) instead of using the index

rocket_status = px.bar(
    status,
    x=['Active', 'Retired'],
    y = status.values,
    color = status.values
)
rocket_status.update_layout(title = 'Active vs Decommissioned Rockets', yaxis_title = "Number of Rockets", coloraxis_showscale = False, yaxis_range =[0,750])

rocket_status.show()
    


# # Distribution of Mission Status
# 
# How many missions were successful?
# How many missions failed?

# In[ ]:





# In[ ]:





# # How Expensive are the Launches? 
# 
# Create a histogram and visualise the distribution. The price column is given in USD millions (careful of missing values). 

# In[ ]:





# In[ ]:





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

# In[ ]:





# In[ ]:





# # Use a Choropleth Map to Show the Number of Failures by Country
# 

# In[ ]:





# In[ ]:





# # Create a Plotly Sunburst Chart of the countries, organisations, and mission status. 

# In[ ]:





# In[ ]:





# In[ ]:





# # Analyse the Total Amount of Money Spent by Organisation on Space Missions

# In[ ]:





# In[ ]:





# In[ ]:





# # Analyse the Amount of Money Spent by Organisation per Launch

# In[ ]:





# In[ ]:





# In[ ]:





# # Chart the Number of Launches per Year

# In[ ]:





# In[ ]:





# # Chart the Number of Launches Month-on-Month until the Present
# 
# Which month has seen the highest number of launches in all time? Superimpose a rolling average on the month on month time series chart. 

# In[ ]:





# In[ ]:





# # Launches per Month: Which months are most popular and least popular for launches?
# 
# Some months have better weather than others. Which time of year seems to be best for space missions?

# In[ ]:





# In[ ]:





# # How has the Launch Price varied Over Time? 
# 
# Create a line chart that shows the average price of rocket launches over time. 

# In[ ]:





# In[ ]:





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




