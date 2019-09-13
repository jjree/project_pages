#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo


# In[2]:


# Locate Chromedriver path
#!which chromedriver


# In[3]:


# Initiate splinter Browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ----
# 
# ### NASA Mars News

# In[4]:


# Initiate new url and browser to visit it
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[5]:


# Extract HTML from site
html = browser.html
soup = bs(html, 'html.parser')


# In[6]:


# Find and print titles of stories
title_list = []
story_list = soup.find_all('ul', class_='item_list')

for story in story_list:
    titles = story.find_all('h3')
    
for title in titles:
    print(title.text)
    title_list.append(title.text)


# In[7]:


# Find and print paragraphs of featured stories
paras_list=[]
paras = story.find_all('div', class_='article_teaser_body')
for para in paras:
    print(para.text)
    paras_list.append(para.text)


# In[8]:


# STORE OUTPUT
mars_news = [{"title": title, "paragraph": para} for title,para in zip(title_list, paras_list)]
print (mars_news) 


# ----
# 
# ### JPL Mars Space Images - Featured Image

# In[9]:


# Initiate new url and browser to visit it
url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url1)


# In[10]:


# Extract HTML from site
html1 = browser.html
soup1 = bs(html1, 'html.parser')


# In[11]:


# Locate images
articles = soup1.find('ul', class_='articles').find_all('li', class_='slide')

# Find URL and store into 'featured_image_url' list
featured_image_url = []
try:
    for art in articles:
        featured_image = art.a['data-fancybox-href']

        featured_image_url.append("https://www.jpl.nasa.gov" + featured_image)
        print (f"https://www.jpl.nasa.gov{featured_image}")
    
except AttributeError as e:
    print(e)

# STORE OUTPUT
mars_img = featured_image_url
mars_img


# ----
# 
# ### Mars Weather

# In[12]:


# Initiate new url and browser to visit it
url2 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url2)


# In[13]:


# Extract HTML from site
html2 = browser.html
soup2 = bs(html2, 'html.parser')


# In[14]:


# Find and print Mars Weather
mars_weather = []
mars_weather_all = (soup2.find_all('div', class_='js-tweet-text-container'))

for weather in mars_weather_all:
    print(weather.text)
    mars_weather.append(weather.text.strip())

# STORE OUTPUT
print(mars_weather)


# ----
# 
# ### Mars Facts

# In[15]:


# Initiate new url
url3 = 'https://space-facts.com/mars/'


# In[16]:


# Extract HTML from site
tables = pd.read_html(url3)
print(tables)


# In[17]:


# Create DF of table1
mars_table1_df = tables[0]
print(mars_table1_df)


# In[18]:


# Convert table1 to HTML
mars_table1_HTML = mars_table1_df.to_html()
print(mars_table1_HTML)


# In[19]:


# Create DF of table 2
mars_table2_df = tables[1]
print(mars_table2_df)


# In[20]:


# Convert table2 to HTMl
mars_table2_HTML = mars_table2_df.to_html()
print(mars_table2_HTML)


# In[21]:


# STORE OUTPUT
mars_facts = [mars_table1_HTML, mars_table2_HTML]
print(mars_facts)


# ----
# 
# ### Mars Hemispheres
# 

# In[22]:


# Initiate new URL
url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url4)


# In[23]:


# Extract HTML from site
html4 = browser.html
soup4 = bs(html4, 'html.parser')

# Identify links to be visited
links_container = soup4.find_all('div', class_='item')

# Visit each site obtained above and extract Title and full-res image URLs
hemisphere_image_urls = []

for lc in links_container:
    # Find link to visit and visit it
    link = lc.a['href']
    full_link = "https://astrogeology.usgs.gov" + link
    browser.visit(full_link)
    click_soup = bs(browser.html, 'html.parser')
    
    # Find title
    title = click_soup.find('h2').text.strip('Enhanced').rstrip()
    print(title)
    
    # Find URL
    img_url = click_soup.find('div', class_='wide-image-wrapper').find('img', class_='wide-image')['src']
    img_url = "https://astrogeology.usgs.gov"+img_url
    print(img_url)
    
    # Append dictionary of title and img_url to list
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
    # Return to starting page (used for testing purposes)
    browser.visit(url4)

# Print list of dictionaries of hemispheres
mars_hemisphere = hemisphere_image_urls
print(mars_hemisphere)


# ## Step 2 - MongoDB and Flask Application

# In[24]:


# Convert ipynb to py file
get_ipython().system('jupyter nbconvert --to script JJREE_mission_to_mars.ipynb')
mars_


# In[33]:


all_info={}
all_info= {"mars_news": mars_news,"mars_img": mars_img, "mars_weather": mars_weather,"mars_facts": mars_facts, "mars_hemispheres": mars_hemisphere}

all_info


# In[ ]:




