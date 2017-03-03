#coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import json 

web_url="http://lvyou.baidu.com/destination/ajax/jingdian?format=ajax&cid=0&playid=0&seasonid=5&surl="
url_fmt= web_url + "%s&pn=%d&rn=%d"
log = os.path.split(os.path.realpath(sys.argv[0]))[0] + os.sep + 'baidulvyou.txt'

file = None


def get_page_content(url):
    try:
        wp = urllib.request.urlopen(url)
        all = wp.read()
        content = str(all.decode("utf8"))
        time.sleep(1)
        return content
    except Exception as e:
        print(e)
        time.sleep(1)
        return page_content(url)

def get_scenic_info(url):
    jsonData = json.loads(get_page_content(url), strict=False)
    for data in jsonData["data"]["scene_list"]:
        price = '0'
        if data['ticket'] is not None:
            price = data['ticket']['price']
        print('{0}:{6}map-{1},{2},${3},{4},{5}'.format( \
            str(data['sname']), \
            str(data['ext']['map_info']), \
            str(data['ext']['avg_remark_score']), \
            str(price), \
            str(data['ext']['address']), \
            str(data['ext']['abs_desc']), \
            str(data['surl'])))
    return jsonData["data"]["scene_list"][0]['sname'].encode()


if __name__ == '__main__':
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 
    file = open(log, 'wb')
    [file.write(get_scenic_info(url_fmt % ('xiamen', i, 30))) for i in range(1,2)]
    file.close()
