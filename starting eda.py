#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[3]:


df = pd.read_csv("C:/Users/DELL/Downloads/imdb_kaggle.csv")
print(df)


# In[4]:


df.head()


# In[5]:


df.tail()


# In[10]:


df.head(100)


# In[17]:


type(df['year'])


# In[18]:


df.info()


# In[22]:


df.memory_usage(deep = True)


# In[23]:


df.describe()


# In[26]:


df.describe(include = 'all')


# In[27]:


df['rank']


# In[28]:


df['name']


# In[ ]:




