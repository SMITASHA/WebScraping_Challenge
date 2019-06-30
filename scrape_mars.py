
# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from splinter import Browser

# Choose the executable path to driver 
def mars():


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    url ="https://mars.nasa.gov/news/"
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest element that contains news title and news_paragraph
    news_title=soup.find('div',class_="content_title").find('a').text
    news_p=soup.find('div',class_="article_teaser_body").text

    # Display scrapped data 
    # print(news_title)
    # print(news_p)

    news_dict = {"news_title": news_title, "news_p": news_p}

    # ## JPL Mars Space Images - Featured Image




    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
            
    browser.visit(jpl_url)





    #HTML Object
    html_image=browser.html
    soup_img=BeautifulSoup(html_image,'html.parser')
    #Find the image url for the current Featured Mars Image

    image_soup=soup_img.find('div',class_="carousel_items")
    image_url=image_soup.find('article')['style']
    featured_image_url=image_url.replace("background-image: url('","").replace("');","")            

    #background-image: url('/spaceimages/images/wallpaper/PIA18903-1920x1200.jpg');
    # print(featured_image_url)

    image_dict={"featured_image_url":featured_image_url}

    # ## Mars Weather

    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)


    #HTML Object
    html_weather=browser.html
    soup_weather=BeautifulSoup(html_weather, 'html.parser')

    # print(soup_weather)

    # Find all elements that contain tweets
    latest_tweets = soup_weather.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            # print(weather_tweet)
            weather_tweet_dict={"weather_tweet":weather_tweet}
            break
        else: 
            pass

    # ## Mars Facts
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    mars_df.to_html()
    # Display mars_df
    #mars_df
    facts_dict = mars_df.to_dict(orient='dict')  # Here's our added param      


    # ## Mars Hemispheres




    hemisphere_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)


    #HTML Object
    html_hemisphere=browser.html
    soup_hemisphere=BeautifulSoup(html_hemisphere, 'html.parser')
    img_soup=soup_hemisphere.find_all('div',class_='item' )
    # print(img_soup)
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    hemisphere_base_url="https://astrogeology.usgs.gov"
    for i in img_soup:
        # Store title
        title=i.find("h3").text
        # Store link that leads to full image website
        click_url=i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemisphere_base_url+click_url)
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        full_img_soup=browser.html
    
        soup = BeautifulSoup(full_img_soup, 'html.parser')
        # Retrieve full image source 
        img_url = hemisphere_base_url+ soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        

    # Display hemisphere_image_urls

    hemisphere_dict={"hemisphere_image_urls":hemisphere_image_urls}

    mars_dict = {**news_dict, **image_dict, **weather_tweet_dict,**facts_dict, **hemisphere_dict}
    return (mars_dict)
print(mars())