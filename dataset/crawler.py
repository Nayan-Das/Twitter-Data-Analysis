import tweepy
import json

#this function will be used to extract tweets from twitter using tweet ids
#here, api points to tweepy module
def lookup_tweets(tweet_IDs, api):
    tweet_count = len(tweet_IDs) #counting the length of list containing tweet ids
    try:
        #twitter allows extraction of 100 tweets at a single request
        for i in range(int(tweet_count / 100) + 1):
            # Catch the last group if it is less than 100 tweets
            end_loc = int(min((i + 1) * 100, tweet_count))
            sub_array = tweet_IDs[i * 100 : end_loc]
            if not sub_array: break
            if (i * 100) % 1000 == 0:
                print('processed', (i*100), 'tweets')
            #extracting tweets and returning as a generator
            yield api.statuses_lookup(sub_array)
    except tweepy.TweepError as e:
        print('Something went wrong, quitting...')
        print('Error code : ', e, sep = '')

if __name__ == "__main__":
    #To get these tokens, you have to go 'https://apps.twitter.com/' and you have to create a developers account
    #then create an app and on success you will get these tokens

    consumer_key = 'NTJKy8YDvNir3OV3m3CwUzoga'
    consumer_secret = 'YQRDChl05j0xJ9Cj5qIx2CRoYpkc3V4kXe89m5fMYYIaeSriK0'
    access_token = '1047452071597940736-DT3EAQbXXUDMTLUcLAU7mQCSkitvik'
    access_token_secret = 'AwvcmBfWvfs4X3SwIyc7oXEAYvV89nPTD7Hbvg7CiS42N'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #authenticating
    auth.set_access_token(access_token, access_token_secret) #setting accession key

    #initializing api with time limits constraints
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    with open('NepalQuake-test-46K-tweetids.txt', 'r') as f:
        tweet_ids = f.read().strip().split('\n')

    results = lookup_tweets(tweet_ids, api) #calling the crawler

    with open('test.json', 'w') as f:
        for x in results:
            for data in x:
                f.writelines(json.dumps(data._json) + '\n') 
