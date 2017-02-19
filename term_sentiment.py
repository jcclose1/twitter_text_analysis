import sys
import string, re
import json

# Script takes the following arguments:
# 1. TXT file of tab-delimited word-sentiment scores
# 2. TXT or JSON file of tweets pulled from live stream

#sys.stdout = open('term_scores.txt', 'w')

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
    if 'text' in tweets[i].keys():
        texts.append(tweets[i]['text'])

# Define text splitting/cleaning fcn    
def clean(text):
    '''Takes unicode string
       Returns list of cleaned, lowercase strings'''
    text = text.split()
    for i in range(len(text)):
        text[i] = re.sub('\W|\n|\t|\r|^(rt|RT)|^http.*', '', text[i])
        text[i] = string.lower(text[i])
    while '' in text: text.remove('')
    return text

# Clean texts in preparation for scoring
for i in range(len(texts)):
    texts[i] = clean(texts[i])
    
# Define fcn to compute sentiment score for each term in tweet_file
def compute_scores(texts, scores):
    '''Input: list of lists of strings'''
    # Initialize empty list of scores
    all_scores = []
    # Iterate over texts, updating sentiment score along the way
    for word_list in texts:
        sent_score = 0
        for word in word_list:
            if word in scores:
                sent_score += scores[word]
        # Add final score for this text to all_scores list
        all_scores.append(sent_score)
     
    # Build a sorted vocabulary list from text corpus
    vocab = []
    for word_list in texts:
        for word in word_list:
            if word not in vocab:
                vocab.append(word)
    vocab.sort()
    
    # Compute term sentiment score if term not in AFINN-111.txt
    # Write either computed or provided score to stdout
    for word in vocab:
        if word not in scores:
            num_tweets = 0
            num_uses = 0
            cumul_score = 0
            for i in range(len(texts)):
                if word in texts[i]:
                    num_tweets += 1
                    cumul_score += all_scores[i]
                num_uses += texts[i].count(word)
            term_score = ((1.*num_tweets)/(1.*num_uses))*(1.*cumul_score)
            sys.stdout.write(str(word) + ' ' + str(term_score) + '\n')
 
# Get term sentiment scores    
compute_scores(texts, scores)
