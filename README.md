# SMM750 DTVC MTP
## How to start
1. install packages
```bash
pip install -r requirements.txt # install packages
```
2. Install Google Chrome

3. run the code in the main.ipynb


## The structure of the code
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