#!/usr/bin/env python
# coding: utf-8

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from flask import Flask, jsonify, request, url_for, redirect, render_template
import sqlalchemy
import datetime as dt
import os
import csv 
import numpy as np
from flask_pymongo import PyMongo



#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# PyMongo
#################################################

# Initialize PyMongo to work with MongoDBs
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################

    
# * A [landing page](#landing-page) containing:
#   * An explanation of the project.
#   * Links to each visualizations page.
@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template('/index.html', mars_info=mars_info)

@app.route("/scrape")
def scraped():
    mars_info = mongo.db.mars_info
    mars_info_data = scrape()
    mars_info.update({}, mars_info_data, upsert=True)
    return redirect("/", code=302)

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # Locate Chromedriver path
    #!which chromedriver

    # Initiate splinter Browser
    browser = init_browser()

    # ### NASA Mars News

    # Initiate new url and browser to visit it
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Extract HTML from site and parse with BS
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

    # STORE OUTPUT
    mars_news = [{"title": title, "paragraph": para} for title,para in zip(title_list, paras_list)]
    print (mars_news) 

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

    # STORE OUTPUT
    mars_img = featured_image_url
    mars_img

    # ### Mars Weather

    # Initiate new url and browser to visit it
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)

    # Extract HTML from site
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    # Find and print Mars Weather
    mars_weather = []
    mars_weather_all = (soup2.find_all('div', class_='js-tweet-text-container'))

    for weather in mars_weather_all:
        print(type(weather))
        
        print(weather.text.split(' ')[0])
        if (weather.text.strip().replace('\n', ' ').split(' ')[0] == "InSight"):
            mars_weather.append(weather.text.strip().replace('\n', ' '))

    # STORE OUTPUT
    print(mars_weather)

    # ### Mars Facts

    # Initiate new url
    url3 = 'https://space-facts.com/mars/'

    # Extract HTML from site
    tables = pd.read_html(url3)
    print(tables)

    # Create DF of table1
    mars_table1_df = tables[0]
    print(mars_table1_df)

    # Convert table1 to HTML
    mars_table1_HTML = mars_table1_df.to_html()
    # soup_table1 = bs(mars_table1_HTML, 'html.parser')
    # mars_table2_HTML = soup_table1.table
    # for th in soup_table1("th"):
    #     soup_table1.th.decompose()
    print(mars_table1_HTML)

    # Create DF of table 2
    mars_table2_df = tables[1]
    mars_table2_df1 = pd.DataFrame()
    mars_table2_df1["Description"] = mars_table2_df[0]
    mars_table2_df1["Values"] = mars_table2_df[1]
    mars_table2_df1.set_index("Description", inplace=True)
    mars_table2_df = mars_table2_df1
    print(mars_table2_df)

    # Convert table2 to HTMl
    mars_table2_HTML = mars_table2_df.to_html()
    # soup_table2 = bs(mars_table2_HTML, 'html.parser')
    # mars_table2_HTML = soup_table2.table
    # for th in soup_table2("th"):
    #     soup_table2.th.decompose()
    print(mars_table2_HTML)

    # STORE OUTPUT
    mars_facts = [mars_table1_HTML, mars_table2_HTML]
    mars_facts

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
    mars_hemisphere = hemisphere_image_urls
    print(mars_hemisphere)

    # Close the browser after scraping
    browser.quit()

    # ## Step 2 - MongoDB and Flask Application

    # Convert ipynb to py file
    # !jupyter nbconvert --to script JJREE_mission_to_mars.ipynb

    # Function 'scrape' returns dictionary of all scraped information
    all_info={"mars_news": mars_news, \
            "mars_img": mars_img, \
            "mars_weather": mars_weather, \
            "mars_facts": mars_facts, \
            "mars_hemispheres": mars_hemisphere
    }

    return all_info

# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)



