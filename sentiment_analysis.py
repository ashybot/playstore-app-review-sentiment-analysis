import json
import regex
import pandas as pd
pd.options.display.max_rows = 1000
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import string
import re
import emoji
from pandas_profiling import ProfileReport
import datetime
import argparse
nltk.download('stopwords')

parser = argparse.ArgumentParser()
parser.add_argument('jsonfilename')
parser.add_argument('outputfilename')
parser.add_argument('htmlfilename')
args = parser.parse_args()

# open json file
f = open(args.jsonfilename,"r")
# Return json object as a dictionary
data = json.loads(json.dumps(f.read()))

# iterating through the json list
for i in data:
  print(i)
print(len(data))
df=pd.DataFrame(eval(data))

prof = ProfileReport(df)
prof.to_file(output_file=args.htmlfilename)

df=df[["reviewCreatedVersion", "score","content", "thumbsUpCount"]]

check_total_none=df.isnull().sum()
print(check_total_none)

score_high= df[df["score"]==5]
print("score high:",score_high)

score_mid=df[df["score"]==3]
print("score_mid:",score_mid)

print(df.reviewCreatedVersion.unique())
print(df.reviewCreatedVersion.nunique())

x=(df.groupby('reviewCreatedVersion')['score'].mean())
print(x)

plt.hist(df['score'], bins = 5)
plt.show()

# Lower casing

# Change the reviews type to string
df['content'] = df['content'].astype(str)
# Before lowercasing
print(df['content'][2])
#Lowercase all reviews
df['content']= df['content'].apply(lambda x: x.lower())
print(df['content'][2]) ## to see the difference

 #check if there is any special character
alphabet = string.ascii_letters+string.punctuation
print(df.content.str.strip(alphabet).astype(bool).any())

extracted_emojis=[]

def extract_emojis(s):
    expe = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    #return expe.findall(s)
    return expe.sub(r'',s)

for y in df['content']:
    #print(str(extract_emojis(y)))
    extracted_emojis.append(str(extract_emojis(y)))
print(extracted_emojis)

# stop words

stop_words=stopwords.words('english')
df['extracted_emojis'] = extracted_emojis
df['extracted_emojis']= df['extracted_emojis'].apply(lambda x:x if x not in stop_words else None)
print(df['extracted_emojis'][5])

# stemming

def stemming(x):
    st = PorterStemmer()
    if x is not None:
       for word in x.split():
           st.stem(word)

df['extracted_emojis'].apply(lambda x:stemming(x))
print(df['extracted_emojis'][100])

#Function to calculate sentiment score for whole data set

def senti_sc(x):
    if x is not None:
       return TextBlob(x).sentiment

df["Sentiment_score"]= df["extracted_emojis"].apply(senti_sc)
ss = open(args.outputfilename, "w")
ss.write(str(df.loc[0:,['extracted_emojis','Sentiment_score']]))
ss.close()
f.close()