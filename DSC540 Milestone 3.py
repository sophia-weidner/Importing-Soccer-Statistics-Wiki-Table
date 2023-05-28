#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import xlrd
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


website = "https://en.wikipedia.org/wiki/List_of_most_expensive_association_football_transfers"

r = requests.get(website)
r.status_code


# In[3]:


# Reading page and seeing how many tables are on the page.
soup = BeautifulSoup(r.text, 'html.parser')
tables = soup.find_all('table',class_="wikitable")
len(tables)


# I am going to load in 3 dataframes: the top 50 expensive transfers, the historical progression, and cumulative trasnfers.

# In[4]:


# Loading top 50 expensive.
load_df = pd.read_html(str(tables))
top50_expensive_transfers = load_df[0]
top50_expensive_transfers.head(10)


# In[5]:


# Loading historical progression.
historical_progression = load_df[1]
historical_progression.head(10)


# In[6]:


# Loading cumulative transfers.
cumulative_transfers = load_df[3]
cumulative_transfers.head(10)


# # Data Transformation 1: Adding USD Column to DF 3.
# I would like to add a column to cumulative_transfers indicating the US dollar amount so that it is easier to read and understand. I am starting with this dataset because it is small. I am going to do the same thing to data sets 1 and 2, though those will be more difficult because they have strings such as '[a]' attached.

# In[7]:


cumulative_transfers['Fees(£ mln)'] = (cumulative_transfers['Fees(£ mln)'].str.strip('£').astype(float))
print(cumulative_transfers['Fees(£ mln)'])


# In[8]:


cumulative_transfers['Fees (US)'] = cumulative_transfers['Fees(£ mln)'] * 1.13
cumulative_transfers.head()


# # Data Transformation 2: Adding USD Column to DF 1.
# I am repeating the process above but with top50_expensive_transfers.

# In[9]:


top50_expensive_transfers.head(10)


# In[10]:


top50_expensive_transfers["Fee(£ mln)"] = top50_expensive_transfers["Fee(£ mln)"].str.replace(r'\D+', '', regex=True).astype(float)


# In[11]:


print(top50_expensive_transfers["Fee(£ mln)"])


# In[12]:


top50_expensive_transfers['Fee (US)'] = top50_expensive_transfers['Fee(£ mln)'] * 1.13
top50_expensive_transfers.head()


# # Data Transformation 3: Adding USD Column to DF 2.
# I am repeating the process above but with historical_progression.

# In[13]:


historical_progression.head()


# In[14]:


# historical_progression["Fee (£)"] = historical_progression["Fee (£)"].str.replace(r'\D+', '', regex=True).astype(float)
historical_progression['Fee (£) New'] = historical_progression['Fee (£)'].str[:-4]
historical_progression.loc[historical_progression["Fee (£) New"] == '21,500,000[92]', "Fee (£) New"] = '21,500,000'
historical_progression.loc[historical_progression["Fee (£) New"] == '198,000,000[3', "Fee (£) New"] = '198,000,000'
historical_progression.loc[historical_progression["Fee (£) New"] == '10', "Fee (£) New"] = '100'
historical_progression["Fee (£) New"] = historical_progression["Fee (£) New"].str.replace(r',', '', regex=True).astype(float)
print(historical_progression['Fee (£) New'])

# I removed the last 4 characters of each data point in the Fee column. 
# I then replaced 3 values that were inaccurate due to removing the 4 characters. I then replaced the inaccurate
# values with the correct ones.
# Next, I removed all commas so I could convert the strings to a float.
# Now, I will create the USD column.


# In[15]:


historical_progression['Fee (US)'] = historical_progression["Fee (£) New"] * 1.13
historical_progression.head()


# # Data Transformation 4: Removing Columns from DF1
# The reference column in top50_expensive_transfers is unneccessary as its only purpose is to link it to other tables from the wikipedia article. I am going to drop this column. I am also going to remove the Fee(€ mln) column as I only need the Fee(£ mln) and Fee (US) columns to link all 3 of my dataframes.

# In[16]:


top50_expensive_transfers.head(3)


# In[17]:


top50_expensive_transfers = top50_expensive_transfers.drop('Ref.', axis = 1)


# In[18]:


top50_expensive_transfers = top50_expensive_transfers.drop('Fee(€ mln)', axis = 1)


# In[19]:


top50_expensive_transfers.head(3)


# In[20]:


# Since I see the column year has a reference (2018[b]), I am going to remove the reference using similar code that
# I used above.
top50_expensive_transfers["Year"] = top50_expensive_transfers["Year"].str.replace(r'\D+', '', regex=True).astype(int)


# In[21]:


top50_expensive_transfers.head(3)


# # Data Transformation 5: Renaming Fee (£ mIn) Columns
# Since the column I created is Fee (US), I am going to rename the Fee (£ mIn) columns in all 3 data sets to Fee (UK Pounds)

# In[22]:


# DF 1: top50_expensive_transfers

# Create new column Fee (UK Pounds) with same values as column Fee(£ mln)
top50_expensive_transfers["Fee (UK Pounds)"] = top50_expensive_transfers["Fee(£ mln)"]


# In[23]:


# Drop Fee(£ mln) column.
top50_expensive_transfers = top50_expensive_transfers.drop('Fee(£ mln)', axis = 1)


# In[24]:


top50_expensive_transfers.head(3)


# In[25]:


# Repeating the same process for DF 2: historical_progression


# In[26]:


historical_progression["Fee (UK Pounds)"] = historical_progression["Fee (£) New"]


# In[27]:


historical_progression = historical_progression.drop('Fee (£) New', axis = 1)
historical_progression = historical_progression.drop('Fee (£)', axis = 1)


# In[28]:


historical_progression.head(3)


# In[29]:


# Repeating the same process for DF 3: cumulative_transfers


# In[30]:


cumulative_transfers["Fee (UK Pounds)"] = cumulative_transfers["Fees(£ mln)"]


# In[31]:


cumulative_transfers = cumulative_transfers.drop("Fees(£ mln)", axis = 1)


# In[32]:


cumulative_transfers.head(3)


# In[33]:


cumulative_transfers.to_csv(r'/Users/sophiaweidner/Downloads/df_2.csv', index=False)
historical_progression.to_csv(r'/Users/sophiaweidner/Downloads/df_3.csv', index=False)
top50_expensive_transfers.to_csv(r'/Users/sophiaweidner/Downloads/df_4.csv', index=False)


# In[ ]:




