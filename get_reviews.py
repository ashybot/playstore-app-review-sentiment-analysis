from google_play_scraper import Sort, reviews
import argparse
from collections import Counter
import pandas as pd
from nltk import FreqDist
import matplotlib.pyplot as plt
import seaborn as sns
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('appid')
args = parser.parse_args()

apps = dict()
apps["com.facebook.katana"] = "facebook"
apps["com.instagram.android"] = "instagram"
apps["com.zhiliaoapp.musically"] = "tiktok"
apps["com.linkedin.android"] = "linkedin"
apps["com.twitter.android"] = "twitter"
apps["org.joinmastodon.android"] = "mastodon"
apps["co.vero.app"] = "vero"
apps["org.thoughtcrime.securesms"] = "signal"
apps["com.mewe"] = "mewe"
apps["co.triller.droid"] = "triller"

result, continuation_token = reviews(
    args.appid,
    lang='en', # defaults to 'en'
    country='us', # defaults to 'us'
    sort=Sort.MOST_RELEVANT, # defaults to Sort.NEWEST
    count=1000, # defaults to 100
    filter_score_with=5 # defaults to None(means all score)
)

# If you pass "continuation_token" as an argument to the reviews function at this point,
# it will crawl the items after 3 review items.

result, _ = reviews(
    args.appid,
    continuation_token=continuation_token # defaults to None(load from the beginning)
)

print(result)

df = pd.DataFrame(result)

def freq_words(x, terms = 30):
  all_words = ' '.join([text for text in x])
  all_words = all_words.split()
  
  fdist = FreqDist(all_words)
  words_df = pd.DataFrame({'word':list(fdist.keys()), 'count':list(fdist.values())})
  
  # selecting top 20 most frequent words
  d = words_df.nlargest(columns="count", n = terms) 
  plt.figure(figsize=(25,5))
  ax = sns.barplot(data=d, x= "word", y = "count")
  ax.set(ylabel = 'Count')
  plt.savefig(apps[args.appid]+"_common.png")
  #plt.show()

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

# function to remove stopwords
def remove_stopwords(rev):
  rev_new = " ".join([i for i in rev if i not in stop_words])
  return rev_new

# remove short words (length < 3)
df['content'] = df['content'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))

# remove stopwords from the text
reviews = [remove_stopwords(r.split()) for r in df['content']]

# make entire text lowercase
reviews = [r.lower() for r in reviews]

#freq_words(reviews, 35)

nlp = spacy.load('en_core_web_sm')
nlp.disable_pipes('ner', 'parser')

def lemmatization(texts, tags=['NOUN', 'ADJ']):
    output = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        output.append([token.lemma_ for token in doc if token.pos_ in tags])
    return output
  
tokenized_reviews = pd.Series(reviews).apply(lambda x: x.split())
print(tokenized_reviews[1])
reviews_2 = lemmatization(tokenized_reviews)
print(reviews_2[1])

reviews_3 = []
for i in range(len(reviews_2)):
    reviews_3.append(' '.join(reviews_2[i]))

df['content'] = reviews_3

freq_words(df['content'], 35)

'''
reviews = ""
for review in result:
    reviews += review['content'] + "\n"

# split() returns list of all the words in the string
split_it = reviews.split()
# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)
# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common(4)
print(most_occur)
'''