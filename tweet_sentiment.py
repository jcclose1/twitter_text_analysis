import sys
import string, re
import json

# Script takes the following arguments:
# 1. TXT file of tab-delimited word-sentiment scores
# 2. JSON file of tweets pulled from live stream

sys.stdout = open('sent_scores.txt', 'w')

sent_file = open(sys.argv[1])
tweet_file = open(sys.argv[2])

# Define fcn to generate 'word':score dictionary from sent_file
def make_dict(sent_file):   
    scores = {} # initialize empty dictionary
    for line in sent_file:
      term, score  = line.split("\t")  # The file is tab-delimited
      scores[term] = int(score)  # Convert score to integer
    return scores

scores = make_dict(sent_file)

# Load tweets iteratively into list        
tweets = []
for line in tweet_file:
    tweets.append(json.loads(line))

# Extract text from each tweet
texts = []
for i in range(len(tweets)):
    if 'text' in tweets[i].keys(): # Not all tweets have 'text' key
        texts.append(tweets[i]['text'])

# Define text splitting/cleaning fcn    
def clean(text):
    '''Takes unicode string'''
    text = text.split()
    for i in range(len(text)):
        text[i] = re.sub('\W|\n|\t|\r|^(rt|RT)|^http.*', '', text[i])
        text[i] = string.lower(text[i])
    while '' in text: text.remove('')
    return text

# Clean texts in preparation for scoring
for i in range(len(texts)):
    texts[i] = clean(texts[i])
    
# Define fcn to compute sentiment score for each tweet in tweet_file
def compute_scores(texts, scores):
    '''Input: list of lists of strings'''
    # Initialize empty list of scores
    all_scores = []
    # Iterate over texts
    for word_list in texts:
        sent_score = 0
        # Iterate over words, incrementing sentiment score
        for word in word_list:
            if word in scores:
                sent_score += scores[word]
        # Write score to stdout
        print(str(sent_score))

# Get sentiment scores    
compute_scores(texts, scores)
