#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from requests import get
import pandas as pd
import numpy as np
import time

#Dependencies Splinter
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')
print(soup.prettify())


# In[5]:


#Collect the latest News Title and assign to variable
news_title = soup.find('div', class_='content_title').text.strip()
news_title


# In[6]:


#Collect the latest News Paragraph and assign to variable
news_p = soup.find('div', class_='rollover_description_inner').text.strip()
news_p


# In[7]:


#Set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


#Visit url for JPL Featured Space Image
base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
url2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(url2)
browser.links.find_by_partial_text('FULL IMAGE')


# In[9]:


# Create BeautifulSoup object; parse with 'html.parser'
html = browser.html
soup = bs(html, "html.parser")


# In[10]:


# Find image URL
image_url = soup.find('img', class_="headerimage fade-in")["src"] 
image_url


# In[11]:


# build full url
featured_image_url = base_url + image_url
featured_image_url


# In[12]:


# Visit the Mars Facts webpage
url3 = "https://space-facts.com/mars/"
browser.visit(url3)


# In[13]:


#Scrape tables
table = pd.read_html(url3)[0]
table


# In[14]:


#Convert pandas df to html string
html_table = table.to_html()
html_table


# In[15]:


# Visit the USGS Astrogeology site
base_url2 = "https://astrogeology.usgs.gov/"
url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url4)


# In[17]:


# Create BeautifulSoup object; parse with 'html.parser'
time.sleep(2)

html = browser.html
soup = bs(html,'html.parser')


# In[18]:


#Create a list to hold dictionaries with hemisphere name and url data
hemisphere_image_urls = []


# In[19]:


#Retrieve parent tags for each hemisphere
hemi_items = soup.find_all('div', class_="item")


# In[20]:


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
    if (title and img_src):
        print('-' *40)
        print(title)
        print(img_src)
    #Create a dictionary and append with the results
    hemi_img_dict = {
        'title': title,
        'image_url':img_src
    }
    hemisphere_image_urls.append(hemi_img_dict)

#View dictionary
hemisphere_image_urls


# In[ ]:




