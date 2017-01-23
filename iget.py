#coding=utf-8
import sys
import urllib.request
import re
import time
import os
import io 

topic_url_prefix="https://m.igetget.com/share/audio/aid/"
url_fmt= topic_url_prefix + "%d"



def analysisOnePage(url):
    print(url)
    content = getPageContent(url)
    name, url = get_mp3_url(content)
    if url!='':
        download(url, name)

def getPageContent(url):
    try:
        wp = urllib.request.urlopen(url)
        all = wp.read()
        content = str(all.decode('utf-8','ignore'))
        return content
    except Exception as e:
        print(e)
        return getPageContent(url)

def download(url, name):
    urllib.request.urlretrieve(url, name+'.mp3')  

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')     
    [analysisOnePage(url_fmt % i) for i in range(5000,7000)]
