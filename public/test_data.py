#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from public.readconfig import ReadConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
data_path = os.path.join(proDir, "data.json")


def generate_test_data(devices):
    dict_tmp = {}
    for d in devices:
        dict_tmp[d['serial']] = {}
        dict_tmp[d['serial']]['user_name'] = ReadConfig().get_testdata('user_name')[devices.index(d)]
        dict_tmp[d['serial']]['password'] = ReadConfig().get_testdata('password')[devices.index(d)]
    with open(data_path, "w") as f:
        json.dump(dict_tmp, f, ensure_ascii=False)
        f.close()
    print("Test data data.json generated success")


def get_test_data(d):
    with open(data_path, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data[d.device_info['serial']]


import requests
from bs4 import BeautifulSoup
import re


def get_apk():
    '''

    :return: 返回apk的参数URL、name、path
    '''
    folder = './apk/'
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        pass
    html = requests.get('http://www1.xiaoying.co/Android/vivavideo/vivavideo_install.html')
    soup = BeautifulSoup(html.text, "lxml")
    tmp = soup.find(href=re.compile("xiaoyingtest"))  # 获取下载链接
    apk = {'url': tmp.get('href'),
           'apk_name': tmp.text,
           'apk_path': folder+tmp.text}
    return apk


def download_apk():
    apk = get_apk()
    r = requests.get(apk['url'], 'wb')
    print('from %s \ndownloading  %s ' % (apk['url'],  apk['apk_name']))
    if r.status_code == 200:
        with open("%s" % (apk['apk_path']), "wb") as code:
            code.write(r.content)
        return True
    else:
        print('%s \nCannot GET ' % r.url)
        return False


if __name__ == '__main__':
    # print(get_apk_url())
    # html = requests.get(url)
    # soup = BeautifulSoup(html.text,"lxml")
    # apk = soup.find(href=re.compile("xiaoyingtest"))
    # print(apk.text)
    # apk_url = apk.get('href')
    # print(apk_url)
    print(download_apk())



