from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path': '/Users/konstajokipii/NU_BOOTCAMP/web-scraping-challenge/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Visiting Mars news URL
    NasaMarsNews = 'https://mars.nasa.gov/news/'
    browser.visit(NasaMarsNews)

    # Creating HTML object
    html = browser.html

    # Parsing HTML w/ BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Getting the first item in a list <li> under an unordered list <ul> 
    latest_news = soup.find('li', class_='slide')
    
    # Saving the news item under a <div> container
    news_title = latest_news.find('div', class_='content_title').text

    # Saving the text paragraph in the container with an 'article_teaser_body' class
    news_paragraph = latest_news.find('div', class_='article_teaser_body').text

    # *********************************************************************************************************************

    # Visiting Mars facts URL
    MarsFacts = 'https://space-facts.com/mars/'
    browser.visit(MarsFacts)

    # Creating HTML object
    html = browser.html

    # Using pandas to scrape the table
    table = pd.read_html(html)

    # Slicing the table into a dataframe
    marsfacts_df = table[0]
    marsfacts_df.columns =['Description', 'Value']
    
    # Converting dataframe to HTML table and passing parameters for styling
    html_table = marsfacts_df.to_html(index=False, header=False, border=0, classes="table table-sm table-striped font-weight-light")

    # *********************************************************************************************************************

    # Visiting USGS Astrogeology URL
    MarsHemisphere = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(MarsHemisphere)

    # Creating HTML object
    html = browser.html

    # Parsing HTML w/ BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieing parent containers for each hemisphere 
    hemispheres = soup.find_all('div', class_="item")

    # Creating empty list for storing the python dictionary
    hemisphere_image_data = []

    # For loop through each container
    for hemisphere in range(len(hemispheres)):

        # Using Splinter to click on all links to get image data
        hemisphere_url = browser.find_by_css("a.product-item h3")
        hemisphere_url[hemisphere].click()
        
        # Creating a BeautifulSoup object with the image URL
        image_url = browser.html
        image_soup = BeautifulSoup(image_url, 'html.parser')
        
        # Storing prefix URL for fullsize image links
        prefix_url = 'https://astrogeology.usgs.gov'
        
        # Saving full resolution images into variable
        suffix_url = image_soup.find('img', class_="wide-image")['src']
        
        # Joining URLs
        full_image_url = prefix_url + suffix_url

        # Saving image title into a variable
        image_title = browser.find_by_css('.title').text
        
        # Adding key value pairs to python dictionary and appending to list
        hemisphere_image_data.append({"title": image_title, "img_url": full_image_url})
        
        # Returning to main page
        browser.back()
        
    # Closing browser session  
    browser.quit()

    # *********************************************************************************************************************

    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "mars_fact_table": html_table, 
        "hemisphere_images": hemisphere_image_data
    }

    # Returning results

    return mars_dict