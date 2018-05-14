# import sys

# Install packages
# ! pip install tweepy
# ! pip install textblob

# Import packages
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        #  paste the token and keys here 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            print("Successfull Authentication")
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 200):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            #fetched_tweets = self.api.search(q = query, count = count,page=15)
            fetched_tweets = [status for status in tweepy.Cursor(self.api.search, q=query).items(count)]
            print(" tweets fetched => processing")
            # parsing tweets one by one
            for tweet in fetched_tweets:
                #check for language
                if tweet.lang != "en":
                    continue
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                if len(tweets)==200:
                    return tweets
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def startQuery(argQuery):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    query=argQuery
    positive=[]
    negative=[]
    neutral=[]
    tweets = api.get_tweets(query, count = 500)
    for tweet in tweets:
        if(tweet['sentiment']=="positive"):
            positive.append(tweet['text'])
        if(tweet['sentiment']=="negative"):
            negative.append(tweet['text'])
        if(tweet['sentiment']=="neutral"):
            neutral.append(tweet['text'])
    resultQuery = {"query" : argQuery,"positive":positive,"negative":negative,"neutral":neutral}       
    print("Done: Sending back the data to node server")
    return json.dumps(resultQuery)

def startQuery1(temp):  #for testing API
    print("inside "+temp)
    # x= ["a","b","c"]
    x= {"a":["1","2","3"],"b":["4","5","6"]}
    y =''.join("".join(e) for e in x)
    z=str(x)
    json_string = json.dumps(x)
    print("json string : "+ json_string)
    return json_string