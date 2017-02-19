import sys
import string, re
import json

# Input: Tweets from live stream in TXT or JSON format

#sys.stdout = open('term_frequencies.txt', 'w')

tweet_file = open(sys.argv[1])

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

## Clean texts in preparation for counting word occurrences
for i in range(len(texts)):
    texts[i] = clean(texts[i])                              
                                                                                                
# Build sorted vocab of unique words in corpus
vocab = []
for word_list in texts:
    for word in word_list:
        if word not in vocab:
            vocab.append(word)
vocab.sort()

# Determine num occurrences of all terms in all tweets
all_uses = 0
#print 'num wordlists: %i' % len(texts)
for word_list in texts:
    all_uses += len(word_list)
    #print 'len_wordlist: %i' % len(word_list)
#print 'all_uses: %i' %all_uses
#Determine term frequency of each term
for word in vocab:
    word_uses = 0
    for word_list in texts:
        word_uses += word_list.count(word)
    tf = (1.*word_uses) / (1.*all_uses)
    sys.stdout.write(str(word) + ' ' + str(tf) + '\n')