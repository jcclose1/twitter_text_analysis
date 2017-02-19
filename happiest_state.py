import sys
import string, re
import json


# Script takes the following arguments:
# 1. TXT file of tab-delimited word-sentiment scores
# 2. TXT or JSON file of tweets pulled from live stream

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

# Load tweets into list        
tweets = []
for line in tweet_file:
    tweets.append(json.loads(line))

# Define fcn to compute average sentiment score for list of tweets
def compute_scores(texts, scores):
    '''Input: list of word lists'''
    # Initialize cumulative score 
    cumul_score = 0
    # Iterate over word lists
    for word_list in texts:
        for word in word_list:
            if word in scores:
                cumul_score += scores[word]
    avg_score = (1.*cumul_score)/(1.*len(texts))
    return avg_score

# Define text splitting/cleaning fcn    
def clean(text):
    '''Takes unicode string'''
    text = text.split()
    for i in range(len(text)):
        text[i] = re.sub('\W|\n|\t|\r|^(rt|RT)|^http.*', '', text[i])
        text[i] = string.lower(text[i])
    while '' in text: text.remove('')
    return text
            
# Subset tweets having location metadata
has_loc = []
for i in range(len(tweets)):
    if 'user' in tweets[i].keys() and tweets[i]['user']['location'] != None:
        has_loc.append(tweets[i])

# Assign U.S. state abbreviations to a list        
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# Build a dictionary containing tweet count and list of tweet texts
# for each U.S. state
state_count = {}                    
for i in range(len(has_loc)):
    split_loc = has_loc[i]['user']['location'].split()
    if len(split_loc)==2 and re.match('^[A-Z]{2}$',split_loc[1])!=None and \
    split_loc[1] in states:
        state = split_loc[1]
        if state not in state_count:
            state_count[state] = {'count':1, 'tweets':[], 'avg_score':0}
        else:
            state_count[state]['count'] +=1
            state_count[state]['tweets'].append(has_loc[i]['text'])
            
# Clean texts in preparation for scoring
for state in states:
    if state in state_count.keys():
        for i in range(len(state_count[state]['tweets'])):
            state_count[state]['tweets'][i] = clean(state_count[state]['tweets'][i])     

# Compute average state sentiment scores
for state in states:
    if state in state_count.keys() and state_count[state]['tweets'] != []:
        state_count[state]['avg_score'] = compute_scores(state_count[state]['tweets'], scores)
    
# Print out 'happiest' state
happiest_score = 1e-20
happiest_state = ''
for state in states:
    if state in state_count.keys():
        if state_count[state]['avg_score'] > happiest_score:
            happiest_score = state_count[state]['avg_score']
            happiest_state = state
sys.stdout.write(str(happiest_state))

    


