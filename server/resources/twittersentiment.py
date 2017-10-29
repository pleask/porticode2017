import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy


def str_join(*args):
    return ''.join(map(str, args))


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'GWcosdkFXdfLpplAT6460uTKZ'
        consumer_secret = 'LrGdA0rKwgGbpK3K9w5T9WG86mYiJVkHqNxUb3Ov9EVNOPGmiE'
        access_token = '863824274-hsEGAXmtkeyEJl9ejQXLd3HjPeZHRQdXREKkFC6J'
        access_token_secret = 'pLvGqNt9OdYDdTb4PR140GazNf6vaiviCKI9ZCXKZ3XQi'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


    sentiment = []

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment

        self.sentiment.append(analysis.sentiment.polarity)

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 100):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
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

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(word):

    # in case length of tweets found here is 0
    posTweetsCompany = 0
    negTweetsCompany = 0
    posTweetsStock = 0
    negTweetsStock = 0
    posTweetsBlank = 0
    negTweetsBlank = 0

    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = str_join(word, ' company'), count = 1000)

    if tweets is not None:
        if len(tweets) != 0:

            # picking positive tweets from tweets
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            # percentage of positive tweets
            #print("Positive tweets percentage (company): {} %".format(100*len(ptweets)/len(tweets)))
            posTweetsCompany = 100*len(ptweets)/len(tweets)
            # picking negative tweets from tweets
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
            # percentage of negative tweets
            #print("Negative tweets percentage (company): {} %".format(100*len(ntweets)/len(tweets)))
            negTweetsCompany = 100*len(ntweets)/len(tweets)

        # calling function to get tweets
    tweets = api.get_tweets(query = str_join(word, ' stock'), count = 1000)

    if tweets is not None:
        if len(tweets) != 0:

            # picking positive tweets from tweets
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            # percentage of positive tweets
            #print("Positive tweets percentage (stock): {} %".format(100*len(ptweets)/len(tweets)))
            posTweetsStock = 100*len(ptweets)/len(tweets)
            # picking negative tweets from tweets
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
            # percentage of negative tweets
            #print("Negative tweets percentage (stock): {} %".format(100*len(ntweets)/len(tweets)))
            negTweetsStock = 100*len(ntweets)/len(tweets)

        # calling function to get tweets
    tweets = api.get_tweets(query = word, count = 1000)

    if tweets is not None:
        if len(tweets) !=0:

            # picking positive tweets from tweets
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            # percentage of positive tweets
            #print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
            posTweetsBlank = 100*len(ptweets)/len(tweets)
            # picking negative tweets from tweets
            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
            # percentage of negative tweets
            #print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
            negTweetsBlank = 100*len(ntweets)/len(tweets)


    posOverall = 0.1*posTweetsBlank + 0.3*posTweetsCompany + 0.6*posTweetsStock
    negOverall = 0.1*negTweetsBlank + 0.3*negTweetsCompany + 0.6*negTweetsStock

    sentiment = api.sentiment

    #print("Overall positive percentage:", posOverall)
    #print("Overall negative percentage:", negOverall)
    #print("Average polarity score:", numpy.mean(sentiment))

    d = {"company": word, "positive": posOverall, "negative":negOverall, "score":numpy.mean(sentiment),
         "posComp": posTweetsCompany, "negComp": negTweetsCompany, "posSto": posTweetsStock,
         "negSto": negTweetsStock, "posWord":posTweetsBlank, "negWord":negTweetsBlank}

    return(d)

import pandas as pd
twitter_sentiment = pd.read_csv('twittersentiment.csv')
twitter_sentiment = twitter_sentiment.drop(twitter_sentiment.columns[[0]], axis = 1)
def maintwitter(word):
    row = twitter_sentiment.loc[twitter_sentiment['company'] == word].to_dict(orient='records')
    return row

# names = pd.read_csv('../NYSEcut.csv')
# names = names.drop('price', axis=1)
# names.columns = ['symbol', 'name']
# names = names.to_dict('records')
#
# import json
# with open('names.json', 'w') as outfile:
#     json.dump(names, outfile)

# import pandas as pd
# df = pd.read_csv("../NYSEcut.csv")
# output = []
# for i, row in df.iterrows():
#     output.append(maintwitter(row['Description']))
#     print(row['Description'])
# output = pd.DataFrame(output)
# outy = pd.concat([df, output], axis=1)
# outy.to_csv('twittersentiment.csv')
