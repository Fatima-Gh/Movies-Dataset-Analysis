#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.style as style


get_ipython().run_line_magic('matplotlib', 'inline')


# ## Business Questions
# 
# Below are the questions I intend to explore:
# 1. What are the most frequent movie genres? 
# 2. Who are the most casted actors?
# 3. What is the distribution of profits for the top 10 most popular movies?

# ## Data Exploration
# First, I will start by invistigating the data to plan data cleaning and wrangling steps.

# In[3]:


#loading the data into a dataframe
movies = pd.read_csv('tmdb-movies.csv')


# In[4]:


#Printing the first 5 rows of the dataset
movies.head()


# In[5]:


movies.shape


# In[6]:


#Get stat of missing data
movies.isnull().sum()


# In[7]:


movies.isnull().sum().sum()


# In[8]:


#stats on the number of duplicates
sum(movies.duplicated())


# ## Data cleaning
# 
# After exploring the data, I intened on applying the following steps:
# 1. Dropping unused columns ('id', 'imdb_id','homepage','director','production_companies','budget_adj', 'revenue_adj', 'overview', 'keywords', 'tagline', 'vote_count','vote_average').
# 2. Convert missing values into NaNs.
# 3. Dropping NaNs.
# 4. Convert columns to appropriate data formats.
# 5. Drop duplicates.

# In[9]:


#Dropping unused columns
#Columns to be deleted
col_to_be_deleted = ['id', 'imdb_id','homepage','director','production_companies','budget_adj', 'revenue_adj', 'overview', 'keywords', 'tagline', 'vote_count','vote_average']

#Dropping the columns from the movies dataset
movies.drop(col_to_be_deleted, axis=1, inplace=True)


# In[10]:


movies.head()


# In[11]:


movies.info()


# In[12]:


movies.shape


# In[13]:


#Dealing with missing or unknown values
movies.isnull().sum().sum()


# In[14]:


# Converting 0 to NaN for budget and revenue
columns = ['budget', 'revenue']
# Replace 0 with NAN
movies[columns] = movies[columns].replace(0, np.NaN)
# Drop rows which contains NAN
movies.dropna(inplace = True)


# In[15]:


movies.shape


# In[16]:


movies.isnull().sum().sum()


# In[17]:


#After dropping NaNs, we have less than half the number of rows left
#Dropping the duplicates rows
movies.drop_duplicates(keep = 'first', inplace = True)


# In[18]:


movies.shape


# In[19]:


movies.info()


# In[20]:


#Converting columns to appropriate data formats

#Convert release_date to datetime
movies.release_date = pd.to_datetime(movies['release_date'])

#Convert budget and revenue to int
col = ['budget', 'revenue']
movies[col] = movies[col].applymap(np.int64)

movies.dtypes


# ## Answering Business Questions

# ### Question 1: What are the top genres based on movie popularity?

# In[21]:


#Creating a list of gernres  
genres = []

for val in movies['genres']:
    try:
        genres.extend(val.split('|'))
    except AttributeError:
        pass

genres = set(genres)
len(genres)


# In[22]:


genres


# In[23]:


def split_genres(val):
    try:
        if val.find(g) > -1:
            return 1
        else:
            return 0
    except AttributeError:
        return 0


# In[24]:


for g in genres:
    movies[g] = movies['genres'].apply(split_genres)


# In[25]:


movies.head()


# In[26]:


rows = movies.iloc[:, 9:29]
top_genres = rows.apply(pd.value_counts)


# In[27]:


top_genres


# In[28]:


# Initialize the plot
ax = top_genres.iloc[1].sort_values(ascending=False).plot.bar(fontsize = 8, figsize=(12,6), color='#8ad4d4')
# Set a title
ax.set(title = 'Top Genres')
# x-label and y-label
ax.set_xlabel('Type of genres')
ax.set_ylabel('Number of Movies')
# Show the plot
plt.show()


# From the analysis above, we can conclude that the most frequent movie genres are Darama, Comedy, Thriller, Action and Adventure.

# ### Question 2: Who are the most casted actors?

# In[29]:


movies.cast[0].split('|')


# In[30]:


cast = []
for val in movies['cast']:
    try:
        cast.extend(val.split('|'))
    except AttributeError:
        pass
        


# In[31]:


cast = set(cast)
len(cast)


# In[32]:


all_cast = pd.Series(movies['cast'].str.cat(sep = '|').split('|')).value_counts(ascending = False)


# In[33]:


# Initialize the plot
ax = all_cast[:20].plot.bar(fontsize = 8, figsize=(12,6), color='#8ad4d4')
# Set a title
ax.set(title = 'Most Casted Actors')
# x-label and y-label
ax.set_xlabel('Actor name')
ax.set_ylabel('Number of Movies')
# Show the plot
plt.show()


# From the analysis above, we can see that the 5 top most casted actors are:Robert De Niro, Bruce Willis, Samuel L. Jackson, Nicolas Cage, and Matt Damon. 

# ### Question 3: What is the distribution of profits for the top 10 most popular movies?

# Exploring the most popular movies:

# In[34]:


movies.sort_values(ascending=False, by=['popularity'])[:10].plot(kind='bar',x='original_title',y='popularity', figsize=(12,6), color='#7d97ad')


# In[42]:


top_movies_revenue = movies[['original_title','revenue', 'budget', 'popularity']].sort_values(ascending=False, by=['popularity'])[:10]

top_movies_revenue[['original_title','revenue', 'budget']].head()


# In[40]:


top_movies_revenue[['original_title','revenue', 'budget']].sort_values(ascending=False, by=['revenue']).plot(x='original_title',
                                                      kind='bar', 
                                                      color=["#8ad4d4","#7d97ad"],
                                                      rot=45, figsize=(16,8))


# In[ ]:




