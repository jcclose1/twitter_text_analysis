import sys
import string, re
import json

# Input: JSON file of tweets

# Load tweets iteratively into list
tweets = []
for line in open(sys.argv[1], 'r'):
    tweets.append(json.loads(line))
    
# Extract English language tweets from corpus
eng_tweets = []
for i in range(len(tweets)):
    if 'lang' in tweets[i].keys():
        if tweets[i]['lang'] == 'en':
            eng_tweets.append(tweets[i])
            
# Write English tweets iteratively to JSON output file
with open('eng_tweets.json', 'w') as f:
    for i in eng_tweets:
        i = json.dumps(i)
        f.write(i)
        f.write('\n')