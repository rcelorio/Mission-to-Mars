#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path)

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    #setup variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "cerberus_enhanced": get_hemisphere(browser)[0],
        "schiaparelli_enhanced": get_hemisphere(browser)[1],
        "syrtis_major_enhanced": get_hemisphere(browser)[2],
        "valles_marineris_enhanced": get_hemisphere(browser)[3]
    }

    #quit
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    try:
        #begin scrapping
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p
    except AttributeError:
        return None, None
    return news_title, news_p

### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url
    return img_url

def mars_facts():
    #read the mars data table
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
      return None

    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    #df
    return df.to_html() 

def get_hemisphere(browser):
    try:
        # Visit URL directly to avoid the original click
        url = 'https://astrogeology.usgs.gov'
        navigation = '/search/map/Mars/Viking/'

        hemisphere_url = ['cerberus_enhanced',
                           'schiaparelli_enhanced',
                           'syrtis_major_enhance',
                           'valles_marineris_enhanced']
        # initiate list for challenge return
        hemisphere_list = []
        
        #loop through the list and and get each page
        for hemisphere_name in hemisphere_url:
            #visit the complete url with appended hemisphere name
            browser.visit(url + navigation + hemisphere_name)
            html = browser.html
            img_soup = BeautifulSoup(html, 'html.parser')
            img_url = img_soup.select_one('div.wide-image-wrapper \
                                            div.downloads ul li a').get('href')
            img_thumb = img_soup.select_one('div.wide-image-wrapper \
                                            div.downloads img').get('src')
            img_title = img_soup.find("h2", class_='title').get_text()
            #save it for return
            hemisphere_list.append({"title": img_title, "img_url": img_url, "img_thumb": url + img_thumb})
                  
        return hemisphere_list
    except: 
        return None

    


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

