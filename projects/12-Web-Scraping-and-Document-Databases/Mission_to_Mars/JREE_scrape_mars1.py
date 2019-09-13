#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, jsonify, request, url_for, redirect, render_template
import sqlalchemy
import datetime as dt
import os
import csv
import numpy as np


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

    
# * A [landing page](#landing-page) containing:
#   * An explanation of the project.
#   * Links to each visualizations page.

@app.route("/")
def landing():
#    return "TESTING"
    return render_template('/landing_bs1.html')


# In[2]:


# Locate Chromedriver path
#!which chromedriver


# In[3]:
def scrape(){
    # Initiate splinter Browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # ### NASA Mars News
    # Initiate new url and browser to visit it
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Extract HTML from site
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find and print titles of stories
    title_list = []
    story_list = soup.find_all('ul', class_='item_list')

    for story in story_list:
        titles = story.find_all('h3')
        
    for title in titles:
        print(title.text)
        title_list.append(title.text)

    # Find and print paragraphs of featured stories
    paras_list=[]
    paras = story.find_all('div', class_='article_teaser_body')
    for para in paras:
        print(para.text)
        paras_list.append(para.text)

    # OUTPUT
    mars_news = [{"title": title, "paragraph": para} for title,para in zip(title_list, paras_list)]
    # print(mars_news)   

    # ### JPL Mars Space Images - Featured Image

    # Initiate new url and browser to visit it
    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)

    # Extract HTML from site
    html1 = browser.html
    soup1 = bs(html1, 'html.parser')

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

    # ### Mars Weather
    # Initiate new url and browser to visit it
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)

    # Extract HTML from site
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    # Find and print Mars Weather
    mars_weather_all = (soup2.find_all('div', class_='js-tweet-text-container'))

    for weather in mars_weather_all:
        print(weather.text)

    # ### Mars Facts

    # Initiate new url
    url3 = 'https://space-facts.com/mars/'

    # Extract HTML from site
    tables = pd.read_html(url3)
    tables

    # Create DF of table1
    mars_table1_df = tables[0]
    mars_table1_df

    # Convert table1 to HTML
    mars_table1_HTML = mars_table1_df.to_html()
    mars_table1_HTML

    # Create DF of table 2
    mars_table2_df = tables[1]
    mars_table2_df

    # Convert table2 to HTMl
    mars_table2_HTML = mars_table2_df.to_html()
    mars_table2_HTML

    # ### Mars Hemispheres

    # Initiate new URL
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)

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
    print(hemisphere_image_urls)


    # ## Step 2 - MongoDB and Flask Application

    # Convert ipynb to py file
    #!jupyter nbconvert --to script JJREE_mission_to_mars.ipynb

    # Function 'scrape' returns dictionary of all scraped information
    all_info={}


    return all_info
}

# In[ ]:

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)

