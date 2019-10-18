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
from pymongo import MongoClient
import time

# ADDITIONS FOR HEROKU DEPLOYMENT
from selenium import webdriver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)






#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# PyMongo
#################################################

# Initialize PyMongo to work with MongoDBs

# app.config['MONGO_URI'] = os.environ.get('MONGODB_URI') or "mongodb://localhost:27017/mars_db"
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI') or "mongodb://localhost:27017/mars_db"

# mongodb://<dbuser>:<dbpassword>@ds133856.mlab.com:33856/heroku_3n5ckfjb
# client = MongoClient('mongodb://localhost:27017/')
# client = client.heroku_3n5ckfjb
mongo = PyMongo(app) 


#################################################
# Flask Routes
#################################################
    
# * A [landing page](#landing-page) containing:
#   * An explanation of the project.
#   * Links to each visualizations page.
@app.route("/")
def index():
    if (mongo.db.mars_info.find_one() == None):
        mars_info = mongo.db.mars_info
    else:
        mars_info = mongo.db.mars_info.find_one()

    return render_template('index.html', mars_info=mars_info)

@app.route("/scrape")
def scraped():
    mars_info = mongo.db.mars_info
    mars_info_data = scrape()
    mars_info.update({}, mars_info_data, upsert=True)
    return redirect("/", code=302)

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # executable_path = {'executable_path': os.environ.get("CHROMEDRIVER_PATH")}
    return Browser('chrome', **executable_path, headless=True)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    

    # browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # return browser

# def init_browser1():

#     GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
#     CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.binary_location = GOOGLE_CHROME_BIN
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.binary_location = GOOGLE_CHROME_PATH
#     browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
#     return browser


def scrape():
    # Locate Chromedriver path
    #!which chromedriver

    # Initiate splinter Browser
    # browser = init_browser()
    # browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # TESTING Sonyasha
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')
    
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    print('browser is ready')


    #
    # ### NASA Mars News

    # Initiate new url and browser to get it
    url = 'https://mars.nasa.gov/news/'
    browser.get(url)
    time.sleep(3)

    # Extract HTML from site and parse with BS
    html = browser.page_source
    soup = bs(html, 'html.parser')
    print("=========PRINTING SOUP =============================")
    print(soup)

    # Find and print titles of stories
    # titles = []
    # title_list = []
    title = ""
    para = ""

    # story_list = soup.find_all('ul', class_='item_list ')
    story_list = soup.find_all('div', class_='grid_layout')
    print("PRINT STORY LIST")
    print(story_list)

    for story in story_list:
        try: 
            title = story.find('div', class_='content_title').find('a').get_text()
            para = soup.find('article_teaser_body').get_text()
        except AttributeError:
            pass

    #-----------
    # story_list = soup.find_all('ul', class_='item_list ')

    # for story in story_list:
    #     title = story.find('div', class_='content_title').find('a').get_text()
    #     para = story.find('article_teaser_body').get_text()
    #     break
    #-----------
    # title = soup.find('div', class_='content_title').find('a').get_text()
    # para = soup.find('article_teaser_body').get_text()

    # title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title').find('a').get_text()
    # para = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='article_teaser_body').get_text()

    # for story in story_list:
    # title = story_list.find('div', class_='content_title').find('a').text
    # para = story_list.find('article_teaser_body').text

    print(story_list)
    print(title)
    print(para)

    # for title in titles:
    #     print(title.text)
    #     title_list.append(title.text)

    # # Find and print paragraphs of featured stories
    # paras_list=[]
    # paras = story.find_all('div', class_='article_teaser_body')
    # for para in paras:
    #     print(para.text)
    #     paras_list.append(para.text)



    # news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title')\
    # .find('a').get_text()

    # news_p = soup.find('ul', class_='item_list ').find('li', class_='slide')\
    # .find('div', class_='article_teaser_body').get_text()

    # mars_news = [{"title": news_title, "paragraph": news_p}]



    # STORE OUTPUT
    # mars_news = [{"title": title, "paragraph": para} for title,para in zip(title_list, paras_list)]
    mars_news = [{"title": title, "paragraph": para}]
    print (mars_news) 


    # ### JPL Mars Space Images - Featured Image

    # Initiate new url and browser to get it
    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url1)
    time.sleep(3)

    # Extract HTML from site
    html1 = browser.page_source
    soup1 = bs(html1, 'html.parser')

    # Locate images
    articles = soup1.find('ul', class_='articles').find_all('li', class_='slide')

    # Find URL and store into 'featured_image_url' list
    featured_image_url = []

    #full_image
    # browser.click_link_by_id('full_image')
    # html1_1 = browser.click_link_by_text('more info     ')

    link = "https://www.jpl.nasa.gov" + soup1.find('footer').a['data-link']
    browser.get(link)
    html1_1 = browser.page_source
    soup1_1 = bs(html1_1, 'html.parser')
    main_image = soup1_1.find('figure', class_='lede').a['href']
    main_image = "https://www.jpl.nasa.gov" + main_image
    print(main_image)
    featured_image_url.append(main_image)

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

    # Initiate new url and browser to get it
    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.get(url2)

    

    # Extract HTML from site
    html2 = browser.page_source
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
    browser.get(url4)

    

    # Extract HTML from site
    html4 = browser.page_source
    soup4 = bs(html4, 'html.parser')

    # Identify links to be geted
    links_container = soup4.find_all('div', class_='item')

    # get each site obtained above and extract Title and full-res image URLs
    hemisphere_image_urls = []

    for lc in links_container:
        # Find link to get and get it
        link = lc.a['href']
        full_link = "https://astrogeology.usgs.gov" + link
        browser.get(full_link)
        
            

        click_soup = bs(browser.page_source, 'html.parser')
        
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
        browser.get(url4)

        

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
    app.run()



