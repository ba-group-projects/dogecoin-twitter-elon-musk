import pandas as pd
from selenium import webdriver
from dateutil import parser
import numpy as np
import urllib
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException


class TwitterScraper:
    def __init__(self, username: str, password: str, account_to_crawl: str = "elonmusk"):
        # self.headers = 'User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36 Cookie=cookie: personalization_id="v1_gSVoa2Nbh/K0vt79iaFe8g=="; guest_id=v1%3A163523688528436906; kdt=hSpV5VVYWRaGZQ4Tu31u8Kwsp9HqqHFqjbfpU7Jh; auth_token=c3af560b5ea112f86bc873aa1a64e3282bb51319; ct0=23298448b4fb6a3a20e92b408551258e622fb3fe6ecacb9d411adcccd30d06b96d51ffe971b13fd2625d8b44833df656c1dbf5c6a71096e0268a940dfd825fcb4d4df29f5ded7e827cbcc5eade23e993; twid=u%3D1456653804334690305; mbox=session#90e919f2cc4540e0ad839b5f15ab5243#1636130231|PC#90e919f2cc4540e0ad839b5f15ab5243.37_0#1699373179; _ga_34PHSZMC42=GS1.1.1636128371.1.1.1636128380.0; des_opt_in=Y; _ga=GA1.2.1241468194.1635236884; _gid=GA1.2.384053437.1636286611; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D'
        # options = webdriver.ChromeOptions()
        # options.add_argument(self.headers)
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('./resources/chromedriver')
        self.driver.implicitly_wait(10)
        self.base_url = 'https://twitter.com'
        self.url = urllib.parse.urljoin(self.base_url, account_to_crawl)
        self.driver.get(self.url)
        self.login()
        self.driver.get(self.url)
        self.tweet_datetime_list = []
        self.tweet_content_list = []
        self.tweet_like_num_list = []
        self.tweet_retweet_num_list = []
        self.tweet_comment_num_list = []
        self.retweet_list = []
        self.flag = True
        self.last_post_date = None

    def login(self):
        # click login button
        self.driver.find_element_by_xpath('//*[@id="layers"]/div/div[1]/div/div/div/div/div[2]/div/div[1]/a').click()
        sleep(5)
        username = self.driver.find_element_by_xpath(
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        username.send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]').click()
        sleep(5)
        password = self.driver.find_element_by_xpath(
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div/input')
        password.send_keys(self.password)
        # click login button
        self.driver.find_element_by_xpath(
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div').click()
        sleep(5)

    def get_and_parse_all_tweets(self, start_date):
        while self.flag:
            elements = self.get_tweets()
            self.judge_whether_post_time_before_start_time(elements, start_date)
            for tweet in elements:
                try:
                    post_datetime = self.parse_post_time(tweet)
                    content = self.parse_content(tweet)
                    like_num = self.parse_like_num(tweet)
                    retweet_num = self.parse_retweet_num(tweet)
                    comment_num = self.parse_comment_num(tweet)
                    retweet = self.judge_whether_retweet(tweet)
                    self.tweet_datetime_list.append(post_datetime)
                    self.tweet_content_list.append(content)
                    self.tweet_like_num_list.append(like_num)
                    self.tweet_retweet_num_list.append(retweet_num)
                    self.tweet_comment_num_list.append(comment_num)
                    self.retweet_list.append(retweet)
                    print(post_datetime, content, like_num, retweet_num, comment_num, retweet)
                except StaleElementReferenceException:
                    pass
            sleep(5)
            self.scroll_down()

        dfm = pd.DataFrame(
            {"datetime": self.tweet_datetime_list, "content": self.tweet_content_list, "like": self.tweet_like_num_list,
             "retweet": self.tweet_retweet_num_list, "comment": self.tweet_comment_num_list,
             "retweet": self.retweet_list})
        dfm.to_csv("data/tweets.csv", index=False)

    def judge_whether_post_time_before_start_time(self, elements, start_date):
        if self.parse_post_time(elements[-1]) <= start_date:
            self.flag = False
        # if self.parse_post_time(elements[-1]) == self.last_post_date:
        #     self.flag = False
        self.last_post_date = self.parse_post_time(elements[-1])

    def get_tweets(self):
        elements = self.driver.find_elements_by_tag_name("article")
        return elements

    def scroll_down(self):
        self.driver.execute_script("scrollBy(0, 2000);")

    @staticmethod
    def parse_post_time(element):
        return parser.parse(element.find_element_by_tag_name("time").get_attribute("datetime"))

    @staticmethod
    def judge_whether_retweet(element):
        if "Elon Musk Retweeted" in element.text:
            return True
        else:
            return False

    def parse_content(self, element):
        if self.judge_whether_retweet(element):
            return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
                5].text
        else:
            return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
                3].text

    @staticmethod
    def parse_like_num(element):
        if "Show this thread" in element.text:
            return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
                -2].text
        return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
            -1].text

    @staticmethod
    def parse_retweet_num(element):
        if "Show this thread" in element.text:
            return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
                -3].text
        return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
            -2].text

    @staticmethod
    def parse_comment_num(element):
        if "Show this thread" in element.text:
            return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
                -4].text
        return element.find_elements_by_css_selector("[class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']")[
            -3].text


class TwitterCleaner:
    def __init__(self,dfm):
        self.dfm = dfm

    def clean_tweets(self):
        # 8 about doge ,4 about spacex, 0 about shiba
        self.dfm = self.dfm.drop_duplicates()
        self.dfm = self.dfm[self.dfm["content"].apply(lambda x: "doge" in x.lower() if x is not np.nan else False)]
        self.dfm.to_csv("data/tweets_clean.csv", index=False)

if __name__ == '__main__':
    tc = TwitterCleaner(pd.read_csv("data/tweets.csv"))
    tc.clean_tweets()

