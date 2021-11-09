import random
import pandas as pd
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


def web_driver(headless=False):
    option = webdriver.ChromeOptions()
    if(headless == True):
        option.add_argument('--headless')
    option.add_argument('start-maximized')
    option.add_argument('disable-infobars')
    option.add_argument('--disable-extensions')
    driver = webdriver.Chrome(options=option)
    return driver

def scrape_tweets(tweet_urls):
    to_return =[]
    
    for i in range(len(tweet_urls)):
        tweet_url = tweet_urls[i]
        print(f'Scraping URL {str(i+1)}/{str(len(tweet_urls))}: {tweet_url}')
        driver = web_driver()
        driver.get(tweet_url)
        driver.implicitly_wait(5)
        tweets = driver.find_elements_by_xpath('//*[@data-testid="tweet"]')

        for i in range(2):
            tweet = tweets[i].text
            if 'Likes' in tweet:
                to_return.append(tweet)
                break
            else:
                continue
        
        driver.quit()
        time.sleep(2)

    return to_return

def parse_tweets(tweets):
    tweet_contents=[];timestamps=[];retweets=[];quotes=[];likes=[]

    for i in range(len(tweets)):
        print(f'Parsing scraped data: {str(i+1)}/{str(len(tweets))}')
        tweet = tweets[i]
        
        time = tweet.split('\n')[-7].split('·')[0].strip()
        date = tweet.split('\n')[-7].split('·')[1].strip()
        timestamp = datetime.datetime.strptime(date + ' ' + time, '%b %d, %Y %I:%M %p')

        timestamps.append(timestamp)
        retweets.append(format_metric(tweet.split('\n')[-6]))
        quotes.append(format_metric(tweet.split('\n')[-4]))
        likes.append(format_metric(tweet.split('\n')[-2]))

        time_section = tweet.split('\n')[-7]
        tweet_contents.append(tweet.split('@elonmusk\n')[1].split('\n'+time_section)[0].replace('\n',' ').encode("ascii", "ignore").decode())

    to_return = pd.DataFrame(zip(timestamps,tweet_contents,retweets,quotes,likes), columns=['timestamp','tweet_content','retweet_count','quote_count','like_count'])

    return to_return

def format_metric(text):
    text = text.replace(',','')

    if 'K' in text:
        text = text.replace('K','')
        text = float(text) * 1000
    elif 'M' in text:
        text = text.replace('M','')
        text = float(text) * 1000000
    elif 'B' in text:
        text = text.replace('B','')
        text = float(text) * 1000000000
    else:
        text = float(text)
        
    return text

if __name__ == '__main__':
    print('Starting Scrape...')
    tweet_urls = pd.read_csv('data/tweet_url.csv')
    to_parse = scrape_tweets(tweet_urls['tweet_url'])
    scraped_data = parse_tweets(to_parse)
    print('Scrape Success!')

    scraped_data.to_csv('data/dogecoin_tweets.csv', index=False)