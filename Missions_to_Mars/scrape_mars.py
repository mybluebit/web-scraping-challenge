#!/usr/bin/env python
# coding: utf-8

# # Dependencies

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import re


# # Chromdriver Path

# In[2]:


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# ## Windows Users can go with codes below

# In[3]:


### def init_browser():
###    executable_path = {"executable_path": "[path]/chromedriver.exe"}
###    return Browser("chrome", **executable_path, headless=False)


# # NASA Mars News Scraper

# In[4]:

def scrape():

    browser = init_browser()

    # Scraping Latest News from NASA Mars News Site

    # Visiting NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(4)

    # Scraping page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Getting the news part
    news = soup.find_all('div', class_="list_text")[0]

    # Getting the news title
    news_title = news.find(class_="content_title").text

    # Getting the news paragraph
    news_body = news.find(class_="article_teaser_body").text

    # Getting the news date
    news_date = news.find(class_='list_date').text

    # Storing News Collected Data as a dictionary
    news_data= {
        "News Date": news_date,
        "News Title": news_title,
        "News Body" : news_body
    }
        
        
    # Closing the browser after scraping
    browser.quit()


    # # JPL Mars Space Images - Featured Image Scraper

    # In[5]:


    browser = init_browser()

    # Scraping JPL Mars Space Images from JPL website

    # Visiting JPL Site
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    time.sleep(2)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    # Getting the featured Image Part  
    featured_image_info = soup.find('article', class_="carousel_item")['style']

    # Finding the Image Name
    featured_image_name= (featured_image_info.split("wallpaper/")[1]).split(".jpg")[0]

    # Creating the Featured Image URL
    main_jpl_url = "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/"
    featured_image_url= main_jpl_url + featured_image_name + ".jpg"


    # Closing the browser after scraping
    browser.quit()


    # # Mars Weather Scraper

    # In[6]:


    browser = init_browser()

    # Scraping Mars Weather from Mars Weather Twitter Account

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    time.sleep(10)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    # Finding the latest Tweet about Mars Weather   
    mars_weather = (soup.find('div', attrs={"data-testid": "tweet"}).get_text()).split('InSight ')[1]

    # Closing the browser after scraping
    browser.quit()


    # # Mars Facts Scraper

    # In[7]:



    # Scraping Mars Facts from Space Fact website 

    url_facts ="https://space-facts.com/mars/"


    # Getting the fact table
    tables = pd.read_html(url_facts)
    fact_table = pd.DataFrame(tables[0])

    fact_table = fact_table.rename(columns={
        0 : "Description",
        1 : "Value"
    })

    fact_table.set_index("Description", inplace = True)

    # Creating the html Table
    table_html = fact_table.to_html()

    # Cleaning the table
    table_html= table_html.replace('\n',"")


    # # Mars Hemispheres
    # ## Finding URL of each page

    # In[8]:



    browser = init_browser()

    #Scraping Mars Hemispheres images URL from USGS Astrogeology Site  
    url_full_img = "https://astrogeology.usgs.gov"
    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_usgs)

    time.sleep(4)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    # Finding the URL of each Hemispheres Images
    url_list= []
    for x in range (8):
        if (x % 2) == 0:
            url_image = soup.find('div', class_="collapsible results").find_all('a')[x]['href']
            full_url = url_full_img + url_image
            url_list.append(full_url)


    # Closing the browser after scraping
    browser.quit()


    # # Mars Hemispheres
    # ## Title & URLs

    # In[9]:



    # Scraping Mars Hemispheres Infos from USGS Astrogeology Site

    url_full_img = "https://astrogeology.usgs.gov"

    final_hemispheres_info=[]

    # Finding the URL & Title of each Hemispheres Images in full size
    for url in url_list:
        browser = init_browser()
        browser.visit(url)

        time.sleep (4)

        # Scraping page into Soup
        html= browser.html
        soup= bs(html, "html.parser")

        # Finding the URL of each Hemispheres Images in full size
        src_image = soup.find('img', class_="wide-image")['src']
        url_final_image = url_full_img + src_image

        # Finding the Title of each Hemispheres Images in full size
        image_title = soup.find('h2', class_="title").get_text()

        #Creating a dictionary of Info
        dic = {"Title": image_title ,
            "Image_URL": url_final_image}

        final_hemispheres_info.append(dic)

        # Closing the browser after scraping
        browser.quit()


    # # Final Dictionary of All Gathered Data

    # In[10]:


    # Final Dictionary of All Gathered Data
    mars_data = {
        "news_date": news_date,
        "news_title": news_title,
        "news_p": news_body,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": table_html,
        "hemisphere_image_title_1": final_hemispheres_info[0]["Title"],
        "hemisphere_image_url_1": final_hemispheres_info[0]["Image_URL"],
        "hemisphere_image_title_2": final_hemispheres_info[1]["Title"],
        "hemisphere_image_url_2": final_hemispheres_info[1]["Image_URL"],
        "hemisphere_image_title_3": final_hemispheres_info[2]["Title"],
        "hemisphere_image_url_3": final_hemispheres_info[2]["Image_URL"],
        "hemisphere_image_title_4": final_hemispheres_info[3]["Title"],
        "hemisphere_image_url_4": final_hemispheres_info[3]["Image_URL"]
    }


    # In[11]:


    return (mars_data)


    # In[ ]:




