![banner image](https://nairametrics.com/wp-content/uploads/2021/12/Elon-Musk-Dogecoin.jpeg)
# Elon Musk's Influence on DogeCoin
Dogecoin is a cryptocurrency created in 2013, featuring the famous “Doge” meme both in its name and on the logos. Although it was first created as a way to make fun of other cryptocurrencies, Dogecoin saw its emergence as a digital investment. On 28th January 2021, Dogecoin closed at 0.01256. Since then it has grown substantially, peaking at 0.7319 on 7th May 2021.

On the 20th December 2020 he infamously tweeted, “One word: Doge”, which soared the Dogecoin price by 20%. Since then, Dogecoin has gained a steady rise in popularity, with Musk credited for being one of the catalysts in its increase in popularity.

![tweet image](https://github.com/ba-group-projects/dogecoin-twitter-elon-musk/blob/main/img/elon-musk-doge-tweet.jpg)

## Table of Contents
* [Installation](#Installation)
* [Project Motivation](#motivation)
* [File Description](#description)
* [Results](#Results)
* [Known Issues](#issue)

## Installation
1. install packages
```bash
pip install -r requirements.txt # install packages
```
2. Install Google Chrome

3. run the code in the main.ipynb
   1. set the `data_source` variable
   2. run the remaining code in the main.ipynb

## Project Motivation <a name="motivation"></a>
TODO

## File Description <a name="description"></a>
The structure of the code is as follows:
- data
  - tweet_url.csv
  - dogecoin_price.csv
  - dogecoin_tweet.csv
  - price_clean_0.25h.csv
- utils
  - \_\_init\_\_.py
  - price.py # encapsulated class for getting price
  - twitter.py # encapsulated class for getting tweets
- main.ipynb # main code
- requirements.txt
- README.md
- cleaned_price_data.csv(the processed data to analyze price)
- cleaned_trend_data.csv(the processed data to analyze trend)

## Results
TODO

## Known Issues <a name="issue"></a>
1. When running the code, if the google-chrome you installed is stable one, it may cause errors like below
    ```
    'FileNotFoundError: [Errno 2] No such file or directory: 'google-chrome''
    ```
    Solution for this is to run the bash command below
    ```bash
    sudo ln -f -s /usr/bin/google-chrome-stable /usr/bin/google-chrome
    sudo chmod +x /usr/bin/google-chrome
    ```
