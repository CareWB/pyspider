#coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import http.cookiejar  

site_url="http://www.mafengwo.cn/"
log = os.path.split(os.path.realpath(sys.argv[0]))[0] + os.sep + 'baidulvyou.txt'

file = None

def get_city_page(city):
    return get_page_content(site_url + city)
    
    
def get_all_plan(content):
    #<a class="plan-title" href="/plan/38137129977e53e2d69d9a8b" target="_blank">厦门5日游</a>
    pattern = re.compile('''<a class="plan-title" href="(.*)" target="_blank">(.*)</a>''',re.M)
    all = re.findall(pattern, content)
    [get_one_kind_plan(site_url + day_plan[0])]
    #for day_plan in all:
    #    file.write('{1}:{0}\n'.format(day_plan[0], day_plan[1]).encode())
    
def get_one_kind_plan(one_kind_url):
    content = get_page_content(one_kind_url)
    
    

def get_page_content(url):
    try:
        wp = urllib.request.urlopen(url)
        all = wp.read()
        content = str(all.decode('utf-8','ignore'))
        time.sleep(1)
        return content
    except Exception as e:
        print(e)
        time.sleep(1)
        return page_content(url)

def get_one_page_scenics(hosturl, posturl, i):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',  
           'Referer' : 'http://www.mafengwo.cn/jd/10132/gonglve.html'}  
    postData = {'sAct' : 'KMdd_StructWebAjax|GetPoisByTag',  
            'iMddid':'10132',
            'iTagId' : '0',
            'iPage' : str(i),
            }  
    cj = http.cookiejar.LWPCookieJar()  
    cookie_support = urllib.request.HTTPCookieProcessor(cj)  
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)  
    urllib.request.install_opener(opener)  
    h = urllib.request.urlopen(hosturl)  
    postData = urllib.parse.urlencode(postData).encode('utf-8')  
  
    request = urllib.request.Request(posturl, postData, headers)  
    response = urllib.request.urlopen(request)
    pattern = re.compile('''<a href=".*poi.*/(.*)" target="_blank" title="(.*)">''',re.M)
    return re.findall(pattern, response.read().decode("unicode_escape"))
    #file.write(text.decode("unicode_escape").encode())
    #print(text.decode("unicode_escape"))

if __name__ == '__main__':
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    file = open(log, 'wb')
    #get_all_plan(get_city_page('xiamen'))
    all = get_one_page_scenics('http://www.mafengwo.cn','http://www.mafengwo.cn/ajax/router.php', 1)
    print(all[0][1])
    content = get_page_content(site_url + 'poi/' + all[0][0])
    file.write(content.encode())
    file.close()
