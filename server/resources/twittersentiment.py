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

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment

        self.sentiment = []
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


def maintwitter(word):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = str_join(word, ' company'), count = 1000)

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
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    #print("\n\nPositive tweets:")
    #for tweet in ptweets[:10]:
    #    print(tweet['text'])

    # printing first 5 negative tweets
    #print("\n\nNegative tweets:")
    #for tweet in ntweets[:10]:
    #    print(tweet['text'])

    #print(posTweetsCompany)
    #print(negTweetsCompany)

        # calling function to get tweets
    tweets = api.get_tweets(query = str_join(word, ' stock'), count = 1000)

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
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    #print("\n\nPositive tweets:")
    #for tweet in ptweets[:10]:
    #    print(tweet['text'])

    # printing first 5 negative tweets
    #print("\n\nNegative tweets:")
    #for tweet in ntweets[:10]:
    #    print(tweet['text'])

    #print(posTweetsStock)
    #print(negTweetsStock)

        # calling function to get tweets
    tweets = api.get_tweets(query = word, count = 1000)

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
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % \ ".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    #print("\n\nPositive tweets:")
    #for tweet in ptweets[:10]:
    #    print(tweet['text'])

    # printing first 5 negative tweets
    #print("\n\nNegative tweets:")
    #for tweet in ntweets[:10]:
    #    print(tweet['text'])

    #print(posTweetsBlank)
    #print(negTweetsBlank)

    posOverall = 0.1*posTweetsBlank + 0.3*posTweetsCompany + 0.6*posTweetsStock
    negOverall = 0.1*negTweetsBlank + 0.3*negTweetsCompany + 0.6*negTweetsStock

    sentiment = api.sentiment

    #print()
    #print("Overall positive percentage:", posOverall)
    #print("Overall negative percentage:", negOverall)
    #print("Average polarity score:", numpy.mean(sentiment))

    d = {"positive": posOverall, "negative":negOverall, "score":numpy.mean(sentiment), "posComp": posTweetsCompany, "negComp": negTweetsCompany, "posSto": posTweetsStock, "negSto": negTweetsStock, "posWord":posTweetsBlank, "negWord":negTweetsBlank}

    return(d)
