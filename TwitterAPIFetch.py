from datetime import datetime
import logging.config
import os
import uuid

from dotenv import load_dotenv
import pandas as pd
import tweepy

from config import config


load_dotenv(verbose=True)
uuid_str = str(uuid.uuid4()).upper()


class TwitterAPIFetch:
    """
    __init__ params:
        - number_of_tweets_to_pull: the # of tweets that are pulled in total
        - hashtag: the hashtag that is queried to find tweets
        - start_date: the start date to start looking from
        - end_date: the end date where to stop looking
    """
    def __init__(
            self,
            number_of_tweets_to_pull: int,
            hashtag: str,
            start_date: str,
            end_date: str = datetime.now().strftime("%Y%m%d%H%M")
    ):
        self.number_of_tweets_to_pull = number_of_tweets_to_pull
        self.hashtag = hashtag
        self.start_date = start_date
        self.end_date = end_date
        self.today_datetime = datetime.now().isoformat()
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_key_secret = os.getenv("TWITTER_API_KEY_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.environment_name = os.getenv("TWITTER_ENVIRONMENT_NAME")
        self.twitter_api = None
        self.tweets_list = [["POSTED_DATE", "TWEET_TEXT", "DATETIME_PULLED"]]
        self.logger = logging.getLogger(__name__ + "." + uuid_str)
        self.set_logger()

    def pipeline(self):
        """
        Process:
            1.) Authenticate Tweepy Twitter API instance
            2.) Fetch Tweets from Full-Archive Search from Twitter
                - convert the responses into 2D List
            3.) Convert responses 2D List into PD DF and Convert to Local CSV
                - ToDo: upload directly to Amazon AWS S3
        """
        self.logger.info("AUTHENTICATING TWITTER API CLIENT")
        auth = tweepy.OAuthHandler(
            self.api_key,
            self.api_key_secret
        )
        auth.set_access_token(
            self.access_token,
            self.access_token_secret
        )
        self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
        self.logger.info("AUTHENTICATED TWITTER API CLIENT SUCCESSFULLY")

        self.logger.info("FETCHING TWEETS")
        self.fetch_tweets()
        self.logger.info("FETCHED TWEETS SUCCESSFULLY")

        self.logger.info(
            "CONVERTING TWEETS LIST TO PD DF AND UPLOADING TO AWS S3 AS CSV"
        )
        self.convert_to_df_and_upload_s3()
        self.logger.info(
            "CONVERTED TWEETS LIST TO PD DF AND UPLOADED TO AWS S3 AS CSV"
        )

    def convert_to_df_and_upload_s3(self):
        """
        converts 2D List to PD Df and eventually will upload to Amazon AWS S3
            Consumes:
                self:
                    tweets_list: the 2D List of tweets
            Produces:
                produces a CSV file of the tweets
        """
        headers = self.tweets_list.pop(0)
        df = pd.DataFrame(data=self.tweets_list, columns=headers)

        # ToDo: Add Amazon AWS S3 bucket link to to_csv PD method below
        df.to_csv("test.csv", index=False)

    def fetch_tweets(self):
        """
        fetches tweets based off given hashtag, start_date, and end_date
            Consumes:
                self:
                    hashtag: the hashtag used in query
                    fromDate: the start date for tweets to fetch
                    toDate: the end date for tweets to fetch
                    number_of_tweets_to_pull: the number of tweets to pull
                    today_datetime: today's datetime in ISO format, used for
                        reference in 2D List/CSV file
        """
        for tweet in tweepy.Cursor(
            self.twitter_api.search_full_archive,
            environment_name=self.environment_name,
            query=self.hashtag,
            fromDate=self.start_date,
            toDate=self.end_date
        ).items(self.number_of_tweets_to_pull):
            self.tweets_list.append(
                [tweet.created_at,
                 tweet.text.encode("utf-8"),
                 self.today_datetime]
            )

    @staticmethod
    def set_logger():
        """
        sets up the logger configuration with basic set up
        """
        logging.config.dictConfig(config['logging_dict'])
