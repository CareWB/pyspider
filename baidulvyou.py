#coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import http.cookiejar  

site_url="https://lvyou.baidu.com/"
log = os.path.split(os.path.realpath(sys.argv[0]))[0] + '\\baidulvyou.txt'

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

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    file = open(log, 'wb')
    get_all_plan(get_city_page('xiamen'))
    file.close()
