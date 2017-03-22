# coding=utf-8
import sys
import urllib.request
import re
import webbrowser
import time
import os
import io
import json
import pymysql


web_site = "http://lvyou.baidu.com/"
web_url = web_site + "destination/ajax/jingdian?format=ajax&cid=0&playid=0&seasonid=5&surl="
url_fmt = web_url + "%s&pn=%d&rn=%d"
hotel_fmt = "http://hotels.ctrip.com/hotel/%s&p%d"
log = os.path.split(os.path.realpath(sys.argv[0]))[
    0] + os.sep + 'baidulvyou.txt'

file = None
hotels = {}
scenics = {}


def get_page_content(url):
    try:
        wp = urllib.request.urlopen(url, timeout=5)
        all = wp.read()
        content = str(all.decode("utf8"))
        time.sleep(1)
        return content
    except Exception as e:
        print(e)
        time.sleep(1)
        return get_page_content(url)


def get_scenics_info(city, url):
    jsonData = json.loads(get_page_content(url), strict=False)
    for data in jsonData["data"]["scene_list"]:
        info = {}
        price = '0'
        if data['ticket'] is not None:
            price = data['ticket']['price']

        info['name'] = str(data['sname'])
        info['city'] = city
        info['id'] = str(data['cid'])
        info['lng'], info['lat'] = str(data['ext']['map_info']).split(',', 1)
        info['score'] = str(data['ext']['avg_remark_score'])
        info['price'] = str(price)
        info['address'] = str(data['ext']['address'])
        info['desc'] = str(data['ext']['abs_desc'])
        info['surl'] = str(data['surl'])

        scenics[info['name']] = info

def get_scenic_detail(scenic):
    type_found = False
    time_fonud = False
    content = get_page_content(web_site + scenic['surl'])
    lines = io.StringIO(content).readlines()
    for line in lines:
        if line.find('景点类型：') > 0:
            amount_found = True
            scenic['type'] = line[line.find('：') + 1:].strip()
        elif line.find('建议游玩：') > 0:
            amount_found = True
            scenic['play_time'] = line[line.find('：') + 1: line.find('&lt;') + 1].strip()
    
        if type_found and time_fonud:
            break

def get_hotels_json_data(content_lines):
    amount_json = None
    detail_json = None
    amount_found = False
    detail_fonud = False

    for line in content_lines:
        if line.find('htllist: ') > 0:
            amount_found = True
            line = line[line.find('['): line.find(']') + 1]
            amount_json = json.loads(
                '{"data":' + line.strip().rstrip(',') + '}', strict=False)
        elif line.find('hotelPositionJSON: ') > 0:
            amount_found = True
            line = line[line.find('['): line.find(']') + 1]
            detail_json = json.loads(
                '{"data":' + line.strip().rstrip(',') + '}', strict=False)

        if amount_found and detail_fonud:
            break

    return amount_json, detail_json


def get_one_page_hotels(city, page_url):
    print(page_url)
    content = get_page_content(page_url)
    lines = io.StringIO(content).readlines()
    amount_json, detail_json = get_hotels_json_data(lines)

    if amount_json is not None:
        for data in amount_json['data']:
            hotels[data['hotelid']] = {}
            hotels[data['hotelid']]['id'] = data['hotelid']
            hotels[data['hotelid']]['city'] = city
            hotels[data['hotelid']]['amount'] = data['amount']

    if detail_json is not None:
        for data in detail_json['data']:
            hotels[data['id']]['name'] = data['name']
            hotels[data['id']]['lat'] = data['lat']
            hotels[data['id']]['lon'] = data['lon']
            hotels[data['id']]['url'] = data['url']
            hotels[data['id']]['address'] = data['address']
            hotels[data['id']]['score'] = data['score']

def insert_into_database():
    conn = pymysql.connect(host='', port=3306, user='',
                           passwd='', db='', use_unicode=True, charset="utf8")
    cursor = conn.cursor()

    sql = """DELETE FROM IMHotel"""
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

    sql = 'INSERT INTO `IMHotel` VALUES '

    for k, v in hotels.items():
        sql += """({id},'{city}','{name}',{score},'{tags}',{must},'{url}','{class_}',{price},{distance},0,'{lng}','{lat}'),""".format(
            id=k, city='XMN', name=v['name'], score=v['score'], tags='经济型', must=1, url=v['url'],
            class_=1, price=v['amount'], distance=100, lng=v['lon'], lat=v['lat'])
    sql = sql[:-1] + ';'
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    sql = """DELETE FROM IMScenic"""
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()

    sql = 'INSERT INTO `IMScenic` VALUES '
    i = 1
    for k, v in scenics.items():
        if 'type' not in v:
            v['type'] = '其他'
            print(v)
        sql += """({id},'{city}','{name}',{score},'{tags}',{free},{must},'{url}','{class_}',{playTime},{price},'{bestFrom}','{bestTo}','{lng}','{lat}','{address}','{desc}',0),""".format(
            id=i, city='XMN', name=v['name'], score=v['score'], tags=v['type'], 
            free=0, must=1, url=v['surl'], class_=1, playTime=3, 
            price=v['price'], bestFrom='09:00', bestTo='17:00', lng=v['lng'], lat=v['lat'],
            address=v['address'], desc=v['desc'])
        i += 1
    sql = sql[:-1] + ';'
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    cursor.close()
    conn.close()


def write_to_file(content):
    for k, v in content.items():
        print(v)


if __name__ == '__main__':
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
    file = open(log, 'wb')

    get_scenics_info('XMN', url_fmt % ('xiamen', 1, 60))
    get_scenics_info('SZX', url_fmt % ('shenzhen', 1, 60))
    get_scenics_info('CAN', url_fmt % ('guangzhou', 1, 60))
    for k, v in scenics.items():
        get_scenic_detail(v)

    [get_one_page_hotels('XMN', hotel_fmt % ('xiamen25', i)) for i in range(1, 5)]
    [get_one_page_hotels('SZX', hotel_fmt % ('shenzhen30', i)) for i in range(1, 5)]
    [get_one_page_hotels('CAN', hotel_fmt % ('guangzhou32', i)) for i in range(1, 5)]
    
    insert_into_database()
    
    file.close()
