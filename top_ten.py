import string, re
import json
import sys

tweet_file = open(sys.argv[1])

# Load tweets into list        
tweets = []
for line in tweet_file:
    tweets.append(json.loads(line))
    
all_tags = {}
for i in range(len(tweets)):
    hashtags =  tweets[i]['entities']['hashtags']
    for j in range(len(hashtags)):
        tag = hashtags[j]['text']
        if tag not in all_tags:
            all_tags[tag] = 1
        else:
            all_tags[tag] += 1
            
top = {}
while len(top) < 10:
    max_val = max(all_tags.values())
    for tag in all_tags.keys():
        if all_tags[tag] == max_val:
            if len(top) < 10:
                top[tag] = all_tags[tag]
                all_tags = {key: value for key,value in all_tags.items() \
                if key not in top.keys()}
            
for key in top.keys():
    sys.stdout.write(str(key) + ' ' + str(top[key]) + '\n')