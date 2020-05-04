
import os
import pandas as pd
import re

#import nltk
from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
#ps = PorterStemmer()
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# Declaring Snowball Stemmer
snowball = SnowballStemmer("english")

 # declaring WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
path = os.getcwd()

all_files = os.listdir(path)

#import chardet
# reading the data from various files
data = []
#path = '.'
#files = [f for f in os.listdir(path) if os.path.isfile(f)]
for f in all_files:
    if f =='Health-Tweets V1.py':
        continue
    else:
        with open(f, "rb") as myfile:
            data1 = myfile.readlines()             
            print(f)            
           # data1[-1]='\nFile End\n'
            data.append(data1)

# flatening the list data
data2 = [j for sub in data for j in sub]

# transforming the data to dataframe
df = pd.DataFrame(data2)
# renaming the column
df.columns = ['Lines']

for i in range(df.shape[0]):
   text =df['Lines'][i] 
   
   if df['Lines'][i] == '':
     df.drop(df['Lines'][i])     
   
   try:
        df['Lines'][i]= df['Lines'][i].decode('utf-8')
   except:
        df['Lines'][i]= df['Lines'][i].decode('windows-1252')  

# df[['binary','date','data']]=df['Lines'].str.split('|',expand=True).apply(lambda x: x.str.strip())

df['lines_split']=''

for i in range(df.shape[0]):
    df['lines_split'][i] =df['Lines'][i].split('|',2)

# to find the length of each lines after splitting
df['length']= df['lines_split'].apply(lambda x: len(x))
    
## Data Preparation Phase (removing Stop Words, Stemming and Lemmatization)

ls = []

def data_cleaning(text,i):
   #text = df['Lines'][i]
   #print (i)
   print(text)
   print(i)
   if text.strip() == '' or df['length'][i] < 3 :
       ls.append(i)
       #print(text)
      # df.drop(df['Lines'][i],axis =0)
       return
   elif (type(text)) == str:
       text = text.lower()
       text = re.sub(r'http:\/\/.*', '', text)
       text = re.sub(r'\r\n', "", text)
       text = re.sub(r"[-()\"#/@;:<>{}`+=~.!?,%'']", "", text)
       text = re.sub(r"[0-9]", "", text)
              # text = text.split()
       text= word_tokenize(text)
               # stemming and removing stop words
       text = [snowball.stem(word) for word in text if not word in set(stopwords.words('english'))]
               # Lemmatization
       text = [lemmatizer.lemmatize(token) for token in text]
       text = ''.join(text)
       if text.strip() == '':
           print(text)
           df.drop(df['Lines'][i],axis =0)
       # stemSentence(text)
       #df['Lines'][i][2]= text
       #clean_review.append(text)
   else:   
        return text
   return text   
 
for i in range(df.shape[0]):
    text = df['Lines'][i]
    #j = df['length'][i]
    df['Lines'][i] = data_cleaning(text,i)

# deleteing all the rows that have no tweet data
os = ls.reverse()

for i in ls:
    print(i)
    df.drop(df.index[i])
df.reset_index()

    
    

