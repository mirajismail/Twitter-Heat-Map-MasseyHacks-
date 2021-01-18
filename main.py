import os
import ssl
import tweepy
from pymongo import MongoClient
import pymongo
# Retriving tokens and keys from environment variables
twitterKey = os.getenv("twitterKey")
twitterSecretKey = os.getenv("twitterSecretKey")
accessToken = os.getenv("twitterAccessToken")
accessTokenSecret = os.getenv("twitterSecretToken")
password = os.getenv("mongoPass")

# Setting MongoDB
client = MongoClient("mongodb+srv://Armaan:" + password + "@cluster-1-dnqxb.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.Twitter
hashtagCollection = db.Hashtags
hashtagCollection.remove({})
# Setting up twitter API
auth = tweepy.OAuthHandler(twitterKey, twitterSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

# Asking the user which hashtag they want to populate the database with
userHashtag = str(input("Which hashtag would you like to populate the database with? #"))
userTweetNum = int(input("How many tweets would you like to find? "))
# Finding tweets
tweetDict = {}
tweetNum = 0
for tweet in tweepy.Cursor(api.search,q="#" + userHashtag,count=100).items():
    if tweet.coordinates is not None:
        tweetNum += 1
        tweetDict[str(tweetNum)] = str(tweet.coordinates)
        if tweetNum == userTweetNum:
            break
print("Tweet search finished!")
hashtagCollection.insert_one(tweetDict)
print("MongoDB upload complete!")