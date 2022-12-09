
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

standing_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

data = requests.get(standing_url)

soup = BeautifulSoup(data.text)

standing_table = soup.select("table.stats_table")[0]

standing_table

links  = standing_table.find_all("a")

links

links = [l.get("href") for l in links]

links

links = [l for l in links if '/squads/' in l]

links

team_urls = [f"https://fbref.com{l}" for l in links]

team_urls

team_url = team_urls[0]
data = requests.get(team_url)

matches = pd.read_html(data.text, match = "Scores & Fixtures")

matches[0].head()


# In[22]:


matches
soup = BeautifulSoup(data.text)
links = soup.find_all("a")

links = [l.get("href") for l in links]


links = [l for l in links if l and "all_comps/shooting/" in l]
links

data = requests.get(f"https://fbref.com{links[0]}")

shooting = pd.read_html(data.text, match = "Shooting")[0]



shooting.head()

shooting.columns = shooting.columns.droplevel()

shooting.head()
team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist","FK", "PK", "PKatt"]], on = "Date")

team_data.head()

matches[0].shape


shooting.shape


# In[37]:


team_data.shape


# In[38]:


years = list(range(2022,2021, -1))


# In[39]:


years


# In[40]:


all_matches = []



standing_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

import time
for year in years:
    data = requests.get(standing_url)
    soup = BeautifulSoup(data.text)
    standing_table = soup.select("table.stats_table")[0]
    
    links = standing_table.find_all("a")
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    previous_season = soup.select("a.prev")[0].get("href")
    standing_url = f"https://fbref.com/{previous_season}"
    
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
        
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match = "Scores & Fixtures")[0]
        
        soup = BeautifulSoup(data.text)
        links = soup.find_all("a")
        links = [l.get("href") for l in links]
        links = [l for l in links if l and "all_comps/shooting/" in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shooting = pd.read_html(data.text, match = "Shooting")[0]
        shooting.columns = shooting.columns.droplevel()
        try:
            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist","FK", "PK", "PKatt"]], on = "Date")
        except ValueError:
            continue
            
        team_data = team_data[team_data["Comp"] == "Premier League"]
        team_data["Season"] = year
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(1)


# In[43]:


team_url.split("/")[-1].replace("-Stats","").replace("-"," ")


match_df = pd.concat(all_matches)


match_df.columns = [c.lower() for c in match_df.columns]



match_df.head()


match_df.shape


match_df.to_json("matches.json")


match_df = pd.read_csv('matches.json')


match_df = match_df.drop('Unnamed: 0',axis=1)

match_df


match_df.tail()


match_df.head()


match_df['round'] = match_df['round'].apply(lambda x: x.replace('\n','').strip().replace('                           ',''))
match_df['round']

match_df=match_df.rename(columns={'referee': 'dagna'})


# In[140]:


# convert dataframe to dict
#dict = match_df.to_dict()
#print(dict)


# In[141]:


##match_df=match_df.set_index('result')


# In[149]:


# Delete a column by column number
# Delete column number 4 (index number 3 in data.columns)
match_df = match_df.drop(columns=match_df.columns[1])


# In[156]:


#match_df = match_df.drop(labels=0, axis=0)

#drop all the columns except time and day
# using 'difference' wee have raises an exception for 2 columns 
#match_df.drop(match_df[match_df.columns.difference(['day', 'time'])], axis=1)


# In[108]:


match_df.duplicated()


# In[109]:


##match_df.isna().sum()


# In[110]:


match_df.describe()


# In[111]:


match_df.columns


# In[ ]:


## match_df = match_df.rename({'date':'ken', 'time':'seat'}, axis='columns')


# In[ ]:


##match_df.columns = ['ken', 'seat']


# In[ ]:


###match_df.columns = match_df.columns.str.replace(' ', '_')


# In[ ]:


match_df.head()


# In[ ]:


match_df.loc[:, ::-1].head()


# In[ ]:


## Drop Columns where all values are missing
match_df.dropna(how='all', axis='columns')

##  Drop Columns by their names using columns parameter
match_df.drop(columns = ['day', 'date'])


# In[ ]:


# new_df = pd.DataFrame(columns=match_df.columns)

##for match_df in pd.read_csv('matches.csv', chunksize=5):
    ##results = match_df.groupby(['Type 1']).count()
    
    ##new_df = pd.concat([new_df, results])
    
    


# In[ ]:


## Split column of values separated by comma into multiple columns
##match_df1 = pd.DataFrame(match_df["time"].str.split(',').fillna('[]').tolist())
##match_df1


# In[ ]:


## to find unique value
 ## match_df.nunique()

match_df.rename(index={0: 'firstgame', 1: 'secondgame',2:'third game'})



#match_df.drop(match_df.columns[[5, 7]], axis=1, inplace=True)
##match_df


# Selecting columns and slicing

#match_df.date


#3match_df[['date']]


#small_df = match_df[['date', 'round']]
#print("Smaller DataFrame:")
#print(small_df.head())



##match_df = pd.DataFrame(match_df["day"].str.split(',').fillna('[]').tolist())



match_df.dtypes

match_df.astype({'season':'float64', 'pkatt':'float'}).dtypes

## match_df.isnull().sum()


import matplotlib as plt
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.preprocessing import StandardScaler


import warnings
warnings.filterwarnings('ignore')

match_df.duplicated().sum()
##match_df.isnull().sum()


# to remove column by user input
remove_col= input(" would u like to 'remove' any column?:")
if remove_col == "yes":
   s_col= input("Select the column you want to  remove:")
   if s_col in match_df.columns and remove_col =="yes":
      print("Column is found and removed")
      match_df = match_df.drop(columns=s_col)
else:
    print("No columns removed")

# Access a column with direct indexing
match_df["round"]

match_df

match_df['day'].value_counts()


labels = match_df['day'].unique().tolist()
values = match_df['day'].value_counts().tolist()

plt.axis("equal")
plt.pie(values, labels=labels, radius=2, autopct='%1.0f%%')
plt.show();

match_df['round'].value_counts()

plt.figure(figsize=(10,8)) # set size of the figure
sns.countplot(data = match_df,x = 'round')

plt.xticks(rotation = 20);


match_df['result'].value_counts(dropna=False)

match_df1=match_df.groupby(['round'],as_index=False)['result'].sum()
match_df1=match_df1.sort_values('result',ascending=False)[:10]
match_df1

#plt.figure(figsize=[15,8])
plt.scatter(match_df1['round'],match_df1['result'],color='r')
plt.xlabel('round',fontsize='large')
plt.ylabel('result',fontsize='small')
plt.xticks(rotation = 90)
plt.title('more matches in match_df1')
plt.show();




