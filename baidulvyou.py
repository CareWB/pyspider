# coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import json

web_site = "http://lvyou.baidu.com/"
web_url = web_site + "destination/ajax/jingdian?format=ajax&cid=0&playid=0&seasonid=5&surl="
url_fmt = web_url + "%s&pn=%d&rn=%d"
log = os.path.split(os.path.realpath(sys.argv[0]))[
    0] + os.sep + 'baidulvyou.txt'

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


def get_scenics_info(url):
    scenics = {}
    jsonData = json.loads(get_page_content(url), strict=False)
    for data in jsonData["data"]["scene_list"]:
        info = {}
        price = '0'
        if data['ticket'] is not None:
            price = data['ticket']['price']

        info['name'] = str(data['sname'])
        info['lng'], info['lat'] = str(data['ext']['map_info']).split(',', 1)
        info['score'] = str(data['ext']['avg_remark_score'])
        info['price'] = str(price)
        info['address'] = str(data['ext']['address'])
        info['desc'] = str(data['ext']['abs_desc'])
        info['surl'] = str(data['surl'])

        scenics[info['name']] = info

    for k, v in scenics.items():
        get_scenic_detail(v)

    return scenics


def get_scenic_detail(scenic):
    content = get_page_content(web_site + scenic['surl'])

    pattern = re.compile('''景点类型：(.*)''', re.I)
    ma = pattern.search(content)
    if ma is not None:
        res = ma.groups()
        scenic['type'] = res[0]

    pattern = re.compile('''建议游玩：(.*)''', re.I)
    ma = pattern.search(content)
    if ma is not None:
        res = ma.groups()
        scenic['play_time'] = res[0]

    return scenic


def write_to_file(scenics):
    print(scenics)
    


if __name__ == '__main__':
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
    file = open(log, 'wb')
    [write_to_file(get_scenics_info(url_fmt % ('xiamen', i, 30)))
     for i in range(1, 3)]
    file.close()
