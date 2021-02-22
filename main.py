from TwitterAPIFetch import TwitterAPIFetch


def main():
    TwitterAPIFetch(
        number_of_tweets_to_pull=1000,
        hashtag="#coloradofires",
        start_date="202006010000"  # YYYYMMddHHmm
    ).pipeline()


if __name__ == "__main__":
    main()
