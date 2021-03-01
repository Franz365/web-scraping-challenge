# Dependencies
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import pymongo

#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_app
collection = db.mars_data

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()

    collection.drop()

    mars_data = {}

    # Visit Mars News URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')
    
    #Get the latest news headline
    news_title = soup.find('div', class_='content_title').text
    
    #Get the latest news article description
    news_p = soup.find('div', class_='rollover_description_inner').text
    
    #Visit JPL URL
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)
    
    #Scrape page into Soup
    html_img = browser.html
    soup = bs(html_img, 'html.parser')
    
    # Find image URL
    image_url = soup.find('img', class_="headerimage fade-in")["src"] 
    image_url

    # build full url
    featured_image_url = base_url + image_url
    featured_image_url

    #Visit Mars Facts
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    #Scrape first table using pandas
    table = pd.read_html(url3)[0]
     
    #Convert pandas df to html string
    html_table = table.to_html()
    html_table = html_table.replace('\n','')
    
    # Mars Hemispheres
    #URLs and connect to browser
    base_url2 = "https://astrogeology.usgs.gov/"
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(url4)
    time.sleep(2)

    html = browser.html
    soup = bs(html,'html.parser')
    
    #Create a list to hold dictionaries with hemisphere name and url data
    hemisphere_image_urls = []
    
    #Retrieve parent tags for each hemisphere
    hemi_items = soup.find_all('div', class_="item")
    
    #Loop through each item in hemi_items[]
    for item in hemi_items:
        
        hemi_img_dict = {}
        
        #Extract title
        hem = item.find('div', class_='description')
        title = hem.h3.text
    
        #Extract image url
        hemi_url = hem.a['href']
        hemi_img_url = base_url2 + hemi_url
        browser.visit(hemi_img_url)
    
        time.sleep(1)
    
        html = browser.html
        soup = bs(html,'html.parser')
        img_src = soup.find('li').a['href']
            
        #Create a dictionary and append with the results
        hemi_img_dict = {
            'title': title,
            'image_url':img_src}
        
        hemisphere_image_urls.append(hemi_img_dict)

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    collection.insert(mars_data)

    return mars_data