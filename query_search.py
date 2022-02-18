import sqlite3
import operator
import os

conn = sqlite3.connect('TermFreq.db')
cur = conn.cursor()
b=cur.execute("SELECT * FROM TFIDF;")
print(b)
desc=cur.description
cols=[]
for y in desc:
    cols.append(y[0])
print (cols)
print ("Enter query keywords:")
q_search = input()
print(q_search)
key_word_search = q_search.lower().split()
# print (key_word_search)
for each_word in key_word_search:
    if each_word not in cols:
        key_word_search.remove(each_word)
print (key_word_search)

summation={}
for z in b:
    summation[z[0]]=0.0
    for each in key_word_search:
        try:
            x=cols.index(each)
            summation[z[0]] += z[x]
        except:
            continue
k=0
for key, value in sorted(summation.items(), key=operator.itemgetter(1), reverse=True):
    if (value != 0.0):
        print (os.getcwd(),str(key))
        print (value)
        k=1
if (k==0):
    print ("No results found! Try using some other keywords")
cur.close()
conn.close()
