import pandas as pd
import time
from selenium import webdriver
import datetime

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

class TwitterScaper:
    def __init__(self, headless=False):
        self.option = webdriver.ChromeOptions()
        if headless == headless:
            self.option.add_argument('--headless')
        self.option.add_argument('start-maximized')
        self.option.add_argument('disable-infobars')
        self.option.add_argument('--disable-extensions')
        # self.options.binary_location = '/usr/bin/google-chrome-stable'
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.implicitly_wait(10)
        self.tweet_url = pd.read_csv('data/tweet_url.csv')["tweet_url"]

    def scrape_tweets(self):
        tweets_list = []
        for url in range(len(self.tweet_url)):
            print(f'Scraping URL {str(url + 1)}/{str(len(self.tweet_url))}: {url}')
            # self.driver = self.web_driver()
            self.driver.get(self.tweet_url[url])
            tweets = self.driver.find_elements_by_xpath('//*[@data-testid="tweet"]')
            for i in range(2):
                tweet = tweets[i].text
                if 'Likes' in tweet:
                    tweets_list.append(tweet)
                    break
                else:
                    continue
        self.driver.quit()
        return tweets_list

    def parse_tweets(self, tweets):
        tweet_contents = []
        timestamps = []
        retweets = []
        quotes = []
        likes = []
        for i in range(len(tweets)):
            print(f'Parsing scraped data: {str(i + 1)}/{str(len(tweets))}')
            tweet = tweets[i]
            time = tweet.split('\n')[-7].split('·')[0].strip()
            date = tweet.split('\n')[-7].split('·')[1].strip()
            timestamp = datetime.datetime.strptime(date + ' ' + time, '%b %d, %Y %I:%M %p')
            timestamps.append(timestamp)
            retweets.append(self.format_metric(tweet.split('\n')[-6]))
            quotes.append(self.format_metric(tweet.split('\n')[-4]))
            likes.append(self.format_metric(tweet.split('\n')[-2]))

            time_section = tweet.split('\n')[-7]
            tweet_contents.append(
                tweet.split('@elonmusk\n')[1].split('\n' + time_section)[0].replace('\n', ' ').encode("ascii",
                                                                                                      "ignore").decode())
        parsed_tweets = pd.DataFrame(zip(timestamps, tweet_contents, retweets, quotes, likes),
                                     columns=['timestamp', 'tweet_content', 'retweet_count', 'quote_count',
                                              'like_count'])

        return parsed_tweets

    @staticmethod
    def format_metric(text):
        text = text.replace(',', '')
        if 'K' in text:
            text = text.replace('K', '')
            text = float(text) * 1000
        elif 'M' in text:
            text = text.replace('M', '')
            text = float(text) * 1000000
        elif 'B' in text:
            text = text.replace('B', '')
            text = float(text) * 1000000000
        else:
            text = float(text)
        return text


if __name__ == '__main__':
    print('Starting Scrape...')
    ts = TwitterScaper(headless=False)
    to_parse = ts.scrape_tweets()
    scraped_data = ts.parse_tweets(to_parse)
    print('Scrape Success!')
    scraped_data.to_csv('data/dogecoin_tweets_test.csv', index=False)
