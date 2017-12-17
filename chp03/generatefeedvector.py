# -*- coding: utf-8 -*-
# @Time    : 2017/12/17 下午11:53
# @Author  : 伊甸一点
# @FileName: generatefeedvector.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import feedparser
import re

def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word != '']

def getwordcounts(url):
    d = feedparser.parse(url)
    word_dic = {}

    for item in d.entries:
        if 'summary' in item:
            summary = item.summary
        else:
            summary = item.description
        words = getwords(item.title + ' ' + summary)
        for word in words:
            word_dic.setdefault(word, 0)
            word_dic[word] += 1
    return d.feed.title, word_dic


apcount={}
wordcounts={}

for feedurl in file('feedlist.txt'):
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
         apcount.setdefault(word,0)
         if count>1:
           apcount[word]+=1
wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5:
        wordlist.append(w)

out=open('blogdata.txt','w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' % word)
    out.write('\n')
for blog,wc in wordcounts.items():
       out.write(blog)
       for word in wordlist:
         if word in wc: out.write('\t%d' % wc[word])
         else: out.write('\t0')
       out.write('\n')