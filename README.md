# Twitter API DU
##### To Use:
1. Create .env file and fill in the following Keys:
    - TWITTER_ACCESS_TOKEN
    - TWITTER_ACCESS_TOKEN_SECRET
    - TWITTER_BEARER_TOKEN
    - TWITTER_API_KEY
    - TWITTER_API_KEY_SECRET 
2. Create Python Virtual Environment
   1. verify you are running a Python3 version
      - `python --version`
      - For reference, I am running `Python 3.7.3` and utilize `Pyenv` for install
   2. Create Python a local venv and venv/ folder
      - `python -m venv ./venv`
   3. Set the new local venv as source
      - Mac Command `source venv/bin/activate`
      - Unknown for Windows Command currently
   4. Install the requirements.txt project dependencies
      - `pip install -r requirements.txt`
      - *** Make Sure That You Have `venv` showing in your terminal before executing install command, otherwise everything will install globally ***
   5. Modify or use the bottom command in main.py and execute main.py
    <br/>
      EXAMPLE:
      <br/>
      
      
      ```python
      if __name__ == "__main__":
            TwitterAPIFetch(
                number_of_tweets_to_pull=1000,
                hashtag="#coloradofires",
                start_date="202006010000"  # YYYYMMddHHmm
            ).pipeline()
      ```
    
