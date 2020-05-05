
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
    
# Data frame with Split Data 

Split_data = df.iloc[:,[1]]
Split_data


df2= pd.DataFrame(Split_data.lines_split.values.tolist(),index=Split_data.index)

# df2 is the new data frame with split data
df2.columns = ['Sl_No','Date','tweets']

## Data Preparation Phase (removing Stop Words, Stemming and Lemmatization)
ls = []

def data_cleaning(text,i):
   print(text)
   print(i)
   if text == '' or text == None:
       print(text)
       ls.append(i)
       return
   else:
       text = text.lower()
       text = re.sub(r'http:\/\/.*',' ', text)
     # text = re.sub(r'\r\n', " ", text)
       text = re.sub(r"[-()\"#/@;:<>{}`+=~.!?,%]",' ', text)
       text = re.sub(r"[0-9]", " ", text)              
       text= word_tokenize(text)
               # stemming and removing stop words
       text = [snowball.stem(word) for word in text if not word in set(stopwords.words('english'))]
               # Lemmatization
       text = [lemmatizer.lemmatize(token) for token in text]
       text = ''.join(text)
       if text.strip() == '':
           ls.append(i)
           return       
   return text
 
for i in range(df.shape[0]):
    text = df2['tweets'][i]
    df2['tweets'][i] = data_cleaning(text,i)

# deleteing all the rows that have no tweet data

if bool(ls):
    ls.reverse()
    for i in ls:
        print(i)
        df2.drop(index= i)
    

df2.reset_index()   
    

