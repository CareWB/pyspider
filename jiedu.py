#coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import http.cookiejar  

topic_url_prefix="http://www.jieduclub.com/"
url_fmt= topic_url_prefix + "forum-57-%d.html"



def analysisOnePage(url):
    content = getPageContent(url)
    topics = getTopics(content)
    print(url)
    print(len(topics))
    print(topics)

    for topic in topics:
        url= getInfosFromTopic(topic)
        print(url)
        thread_content = getPageContent(url)
        url_pre, name = get_mp3_url(thread_content)
        download(url_pre, name)

def getPageContent(url):
    try:
        wp = urllib.request.urlopen(url)
        all = wp.read()
        content = str(all.decode('utf-8','ignore'))
        time.sleep(1)
        return content
    except Exception as e:
        print(e)
        time.sleep(1)
        return getPageContent(url)
    
def getTopics(content):
    start_from = '作者'
    start = content.index(start_from)
    start = -start
    content = content[-start:]
    #print(content)
    
    pattern = re.compile('''<a href="thread-\d*-\d*-\d*.html" onclick="atarget.*>.*</a>''',re.I)
    return re.findall(pattern, content)

def getInfosFromTopic(topic):
    pattern = re.compile('''<a href="(thread-\d*-\d*-\d*.html)" onclick="atarget.*>.*</a>''',re.I)
    res = pattern.search(topic).groups()
    return topic_url_prefix + res[0]
    
def hasKeyString(title):
    for key in keys:
        if title.find(key) > -1:
            return True
    return False
    
def writeToFile(title, url):
    file.write(title + '\n' + url + '\n\n')
    
def webOpen(url):
    if auto_open:
        webbrowser.open_new_tab(url)
        time.sleep(3)
    
def login(hosturl, posturl):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',  
           'Referer' : 'http://www.jieduclub.com/forum.php'}  
    postData = {'fastloginfield' : 'username',  
            'cookietime':'2592000',
            'username' : 'xxxxxx',
            'password' : 'xxxxxx', #你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密  
            }  
    cj = http.cookiejar.LWPCookieJar()  
    cookie_support = urllib.request.HTTPCookieProcessor(cj)  
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)  
    urllib.request.install_opener(opener)  
    h = urllib.request.urlopen(hosturl)  
    postData = urllib.parse.urlencode(postData).encode('utf-8')  
  
    #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
    request = urllib.request.Request(posturl, postData, headers)  
    response = urllib.request.urlopen(request)  
    text = response.read()  
    print(text)  

def download(url_pre, name):
    urllib.request.urlretrieve('http://' + urllib.parse.quote(url_pre+'/'+name), name)  

def get_mp3_url(content):
    #print(content)
    pattern = re.compile('''mp3: "http://(.*)/(.*.mp3)"''',re.I)
    res = pattern.search(content).groups()
    return res[0], res[1]
    

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    hosturl = 'http://www.jieduclub.com/forum.php'
    posturl = 'http://www.jieduclub.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    login(hosturl, posturl)
    
    [analysisOnePage(url_fmt % i) for i in range(1,7)]
    
    #analysisOnePage('http://www.jieduclub.com/thread-2421-1-1.html')
    #file.close()
