#coding=utf-8

import sys
import io
import re
import os
import urllib.request

log = os.path.split(os.path.realpath(sys.argv[0]))[0] + '\\iget.txt'
topic_url_prefix="https://m.igetget.com/share/audio/aid/"
url_fmt= topic_url_prefix + "%d"
file = None

def analysisOnePage(url):
    content = getPageContent(url)
    name, mp3_url = get_mp3_url(content)
    if mp3_url != '':
        #print(name, url)
        writeToFile(name, url)
        #download(mp3_url, name)
        
def getPageContent(url):
    try:
        wp = urllib.request.urlopen(url)
        all = wp.read()
        content = str(all.decode('utf-8','ignore'))
        return content
    except Exception as e:
        print(e)
        return getPageContent(url)
            
            
def get_mp3_url(content):
    title = ''
    url = ''
    pattern = re.compile('''<title>(.*)</title>''',re.I)
    ma = pattern.search(content)
    if ma is not None:
        res = ma.groups()
        if len(res[0]) > 0:
            title = res[0]
                
    pattern = re.compile('''<div id="audio_url" data-src="(.*)" style="display''',re.I)
    ma = pattern.search(content)
    if ma is not None:
        res = ma.groups()
        if len(res[0]) > 0:
            url = res[0]
        
    return title, url.replace('&amp;', '&')
    
def download(url, name):
    urllib.request.urlretrieve(url, name+'.mp3')  
    
def writeToFile(title, url):
    file.write(title + ':' + url + '\n')

if __name__ == '__main__':
    file = open(log, 'a+')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    [analysisOnePage(url_fmt % i) for i in range(6500,7000)]
    file.close()