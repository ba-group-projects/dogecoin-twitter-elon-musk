# Elon Musk's Influence on DogeCoin
TODO: add introduction to dogecoin and elon musk's fascination in the cryptocurrency through tweets

## Table of Contents
* [Installation](#Installation)
* [Project Motivation](#motivation)
* [File Description](#description)
* [Results](#Results)

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

## Known Issues
1. When running the code, if the google-chrome you installed is stable one, it may cause errors like below
    ```
    'FileNotFoundError: [Errno 2] No such file or directory: 'google-chrome''
    ```
    Solution for this is to run the bash command below
    ```bash
    sudo ln -f -s /usr/bin/google-chrome-stable /usr/bin/google-chrome
    sudo chmod +x /usr/bin/google-chrome
    ```
