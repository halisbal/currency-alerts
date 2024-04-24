import tweepy
import os


class Twitter:
    def __init__(self):
        self.consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        self.consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        self.auth = tweepy.OAuth1UserHandler(
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret,
        )
        self.client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )
        self.old_client = tweepy.API(self.auth)

    def post_tweet(self, text, media_path):
        media = self.old_client.media_upload(media_path)
        self.client.create_tweet(text=text, media_ids=[media.media_id])


twitter = Twitter()
