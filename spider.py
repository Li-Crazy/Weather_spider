'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/4/22 18:33
@Software: PyCharm
@File    : spider.py
'''
import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []
def parse_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 "
                      "QQBrowser/10.4.3341.400"
    }
    response = requests.get(url,headers=headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_="conMidtab")
    # print(conMidtab)
    tables = conMidtab.find_all('table')
    for table in tables:
        # print(table)
        # print("+"*30)
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            # print(tr)
            # print("="*30)
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            # print(city)
            temp_td = tds[-2]
            min_temp = int(list(temp_td.stripped_strings)[0])
            ALL_DATA.append({'city':city,'min_temp':min_temp})
            # print({'city':city,'min_temp':min_temp})
        # break

def main():
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
            'http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml',
            'http://www.weather.com.cn/textFC/hz.shtml',
            'http://www.weather.com.cn/textFC/hn.shtml',
            'http://www.weather.com.cn/textFC/xb.shtml',
            'http://www.weather.com.cn/textFC/xn.shtml',
            'http://www.weather.com.cn/textFC/gat.shtml']
    for url in urls:
        parse_url(url)

    # 数据分析排序取最低气温前十
    # def sort_key(data):
    #     min_temp = data['min_temp']
    #     return min_temp
    #
    # ALL_DATA.sort(key=sort_key)
    # print(ALL_DATA)
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    data = ALL_DATA[0:10]
    # print(ALL_DATA)
    # cities = []
    # for city in data:
    #     city = city['city']
    #     cities.append(city)

    cities = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'],data))
    chart = Bar("中国天气最低气温排行榜")
    chart.add('',cities,temps)
    chart.render("temperature.html")

if __name__ == '__main__':
    main()
