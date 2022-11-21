#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: The Movie Database Analysis
# 
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description  
# <p>This is an Imdb dataset containing <b>10866</b> rows and  <b>21</b> rows displaying over 10,000 movies with the vote counts, popularity and revenue. </p>
# 
# **View column names below:**

# In[17]:


df_movies.head(0)


# ### Question(s) for Analysis
# 1. Does the popularity of the movie affect the revenue?
# 2. Which year has the highest number of movies released?
# 3. Which year had the highest  total number of vote count?
# 4. Relationship between vote count and the popularity?
# 5. The name of the movie with the highest  and lowest revenue?
# 6. The name of the movie with the highest and lowest runtime?

# In[43]:


# importing packages.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[19]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
#  #### General Properties
# 

# In[44]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df_movies= pd.read_csv('tmdb-movies.csv') 


# In[45]:


df_movies.head()


# In[22]:


#Check if there are missing values in each column.
df_movies.info()
df_movies.isna().sum()


# In[23]:


#To know how many rows and columns are there in the dataset.
df_movies.shape


# 
# ### Data Cleaning
# 

# **Dropping some column in the dataset using the .drop() function.**
# >**Note:** Missing value found in some columns. Instead of ignoring it, i'll rather fill in with the mean value. 
# I also noticed that all data type seems okay except the **_release_date_** column. So, i'll change to an ISO standard using the **to.datetime() method.** 

# In[24]:


df_movies.drop(['cast', 'director','homepage', 'production_companies', 'tagline', 'overview', 'keywords'], axis = 1, inplace = True)


# In[25]:


#To check
df_movies.head(4)


# In[26]:


#To count duplicates
sum(df_movies.duplicated())


# In[27]:


#Drop duplicates and check 
df_movies.drop_duplicates(inplace = True)
sum(df_movies.duplicated())


# In[28]:


#replacing null values with their respective mean using the fillna()
df_movies = df_movies.fillna(df_movies.mean())


# In[29]:


#Changing release_date dtype

df_movies['release_date'] = pd.to_datetime(df_movies['release_date'])

df_movies.head(4)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 
# ### Research Question 1 (Does the popularity of the movie affect the revenue?)
# <p>The higher the popularity, the higher the revenue?<p/>

# In[30]:


#df_movies.plot(x = 'popularity', y = 'revenue', kind = 'scatter')
df_movies.hist(figsize = (15, 15))


# I needed to get more insights on all the numeric columns in the dataset. So, i created a histogram using the hist() function.

# In[31]:


df_movies.plot(x = 'revenue', y = 'popularity', kind = 'scatter', figsize = (9,6), alpha = 0.5, s = 60)


# **Reasoning section:** The points are seen closer to each other, viewing from the x - axis but not neccesary forming a straight line. Therefore, there's a weak positive correlation here. 

# ### Research Question 2  (Which year has the highest number of movies released?)

# In[32]:


df_movies['release_year'] = df_movies['release_date'].apply(lambda x: x.year)


# In[33]:


movie_year = df_movies.groupby('release_year')['original_title'].count()
movie_year


# In[34]:


#Creating a funtion
def barh_plot(x , y , z):
    x.plot(kind = 'barh', figsize = (15, 15), color = 'blue')
    plt.title(y)
    plt.xlabel (z, fontsize = 15)
    plt.ylabel ('release_year', fontsize = 15)
    
barh_plot(movie_year, 'Year vs. Number of movies', 'count')

#You can use the code below for the same result
# movie_year.plot(kind = 'barh', figsize = (15, 15), color = 'blue')
# plt.title('Year vs. Number of movies')
# plt.ylabel('release_year', fontsize = 15, )
# plt.xlabel('count', fontsize = 15)


# **Reasoning Section:** Here, 2014 seems to be the year with the highest number of movies released. 2015 and 2013 are clearly seen to be the second best.

# ### Research Question 3  (Which year had the highest  total number of vote count?)
# <p>Here, 2013 had the highest total number of vote counts, while 1966 seems to be year with the lowest.<p/>

# In[35]:


year_vote_count = df_movies.groupby('release_year')['vote_count'].sum()
year_vote_count


# In[36]:


barh_plot(year_vote_count, 'Year by Votecount', 'Vote_count')

#You can use the code below for the same result
# year_vote_count.plot(kind = 'barh', figsize = (15, 15))
# plt.title('Year by Votecount')
# plt.ylabel('release_year', fontsize = 15)
# plt.xlabel('Vote_count', fontsize = 15)


# **Reasoning section:** The year 2013 is seen to have the highest total number of vote counts for all movies released in that year. The year 2012, 2014 and 2015 also had higher vote count.

# ### Research Question 4 (Relationship between vote count and the popularity popularity of a movie?)
# 

# In[37]:


df_movies.plot(x = 'vote_count', y = 'popularity', kind = 'scatter', figsize = (8,8), alpha = 0.7)
plt.title('Popularity vs. Vote Count')


# **Reasoning Section**: Most of the points are seen together moving to the right of the x - axis and a straight line can be drawn in the plot. Therefore, there's a strong positive correlation.</p>

# ### Research Question 5 (The name of the movie with the highest  and lowest revenue?)
# 

# In[38]:


maximium = df_movies['revenue'].max()
max_revenue = df_movies.original_title[df_movies['revenue'] == maximium]
print(max_revenue)


# In[39]:


minimium = df_movies['revenue'].min()
min_revenue = df_movies.original_title[df_movies['revenue'] == minimium]

print(min_revenue)


# **Reasoning Section:** I made use of the min() and max() function to find the movies with the highest and lowest revenue. Avatar is the movie with the highest revenue and the result above are the movies that had the lowest revenue.

# ### Research Question 6  (The name of the Movies with the highest and lowest runtime?)
# <p>The movie, "The story of film: An Odyssey" has the highest runtime of 900 minutes. <p/>

# In[40]:


# movie with highest runtime.
maxi= df_movies['runtime'].max()
max_runtime = df_movies.original_title[df_movies['runtime'] == maxi]
print(max_runtime, ':Runtime =', maxi)


# <b><p>The following list below show all movies with a runtime of 0 minutes. <p/></b>

# In[41]:


# movie with highest runtime.
mini= df_movies['runtime'].min()
min_runtime = df_movies.original_title[df_movies['runtime'] == mini]
print(min_runtime, ':Runtime =', mini)


# **Reasoning Section:** I made use of the min() and max() function to find the movies with the highest and lowest runtime. The Story of Film: An Odyssey is the movie with the highest runtime of 900 minutes and the result above are the movies that had the lowest runtime of 0 minutes.

#  

# ## Limitation: 
# Null values were found in this dataset which could create an inaccurate analysis. So, i simply replaced all null values with their respective mean using the mean() function.

# ## Conclusion
# In this analysis, i discovered the following:
# <li>In the movie industry, 2015 had the highest revenue/income.</li>
# <li>The year 2014 had the highest number of movie released. Although, 2013 and 2015 were the second best.</li>
# <li>The number of vote count does not neccessary determine the popularity of the movie.</li>
# <li>The year 2013, had the highest number of vote count.</li>
# <li>In the movie industry, 2015 had the highest revenue/income.</li>
# 

# In[46]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




