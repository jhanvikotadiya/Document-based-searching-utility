import operator
import os
import sqlite3
from os import walk
import math

def create_dictionary(clean_word_list, total_words):
    word_count = {}
    for word in clean_word_list:
        if ((word in word_count) & (word not in stop_word_list)):
            word_count[word] += 1
        elif (word not in stop_word_list):
            word_count[word] = 1

    col=['DocName']
    freq=[doc_list[p]]
    entry=[doc_list[p]]
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1), reverse=True):
        col.append(key)
        entry.append(value)
        freq.append(value/total_words)

    conn = sqlite3.connect('TermFreq.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE if not exists TC (DocName text primary key);')
    cur.execute('CREATE TABLE if not exists TF (DocName text primary key);')
    cur.execute('CREATE TABLE if not exists IDF (word text primary key, idf_value number);')
    cur.execute('CREATE TABLE if not exists TFIDF (DocName text);')


    cols_existing=[]
    a=cur.execute("SELECT * FROM TC;")
    desc = cur.description
    for r in desc:
        cols_existing.append(r[0])

    for y in col:
        if y not in cols_existing:
            cur.execute("ALTER TABLE TC ADD COLUMN '" + y + "' number default 0;")
            cur.execute("ALTER TABLE TF ADD COLUMN '" + y + "' number default 0;")
            cur.execute("ALTER TABLE TFIDF ADD COLUMN '" + y + "' number default 0;")

    cur.execute("INSERT INTO TC " + str(tuple(col)) + " VALUES " + str(tuple(entry)) + ";")
    cur.execute("INSERT INTO TF " + str(tuple(col)) + " VALUES " + str(tuple(freq)) + ";")

    cur.execute("SELECT * FROM TF;")
    b=cur.fetchall()
    i=1
    df=['word_index']
    idf=['word_index']
    ce=len(cols_existing)
    while i<ce:
        df.append(0)
        for z in b:
            if (z[i] != 0):
                df[i]+=1
        idf.append(1 + math.log(n / df[i]))
        #cur.execute("INSERT INTO IDF (word, idf_value) VALUES (" + str(tuple(cols_existing[i],)) + ", " + str(tuple(idf[i],)) + ");")
        i+=1

    for z in b:
        i=1
        wgt=['']
        wgt[0]=z[0]
        while i < ce:
            wgt.append((z[i]) * (idf[i]))
            i+=1
        if (p==(n-1)):
            # print (wgt)
            cur.execute("INSERT INTO TFIDF "+str(tuple(cols_existing))+" values " + str(tuple(wgt)) +";")
    # print ("pass", p)

    cur.execute("SELECT * FROM TFIDF;")
    b=cur.fetchall()
    for z in b:
        print (z)

    cur.close()
    conn.commit()
    conn.close()

def clean_up_list():
    clean_word_list = []
    symbols = "\!@#$%^&*()_+{}:\"<>?,./;'[]-='"
    l=len(symbols)
    for word in word_list[p]:
        for i in range(0, l):
            word = word.replace(symbols[i], "")
        if (len(word) > 0):
            clean_word_list.append(word)
    total_words = len(clean_word_list)
    create_dictionary(clean_word_list, total_words)

f_stop_words = open(r'C:\Users\dell\Desktop\Search Engine\word_count\stopwords.txt','r')
stop_content = f_stop_words.read()
stop_word_list = stop_content.strip().split()
f_stop_words.close()


# strat for loop from here

word_list = []
p = 0
doc_list = os.listdir(r'C:\Users\dell\Desktop\Search Engine\word_count\data_directory')
print(doc_list)
n=len(doc_list)
while (p < n):
    word_list.append([])
    fo = open(r'C:\Users\dell\Desktop\Search Engine\word_count\data_directory\\' + doc_list[p],'r')
    content = fo.read()
  # print (doc_list[p])
  # prints the name of fetched document
    words = content.lower().split()
    for each_word in words:
        word_list[p].append(each_word)
    clean_up_list()
    fo.close()
    p+=1

# end for loop here

# get directory tree => get file name list
 

# files = []
# directories = []
# for (dirpath, dirnames, filenames) in walk(mypath):
#    f.extend(filenames)
