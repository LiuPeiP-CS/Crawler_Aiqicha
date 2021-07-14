# -*- coding:utf-8 -*-

import requests
from time import sleep
import yaml
import json
import os
from Get_Requests import GetRequests


class JsonDownload(object):
    def __init__(self):
        # 初始化对象
        self.dj_get_req = GetRequests()
        self.cn_get_req = GetRequests()

    # 获取网页上的所有内容数据
    def download(self, pid):
        """
        :param pid: 企业的爱企查代码
        :return:
        """
        if pid is None:
            return None
        else:
            return self.download_json(pid)

    # 该方法适用于动态渲染中的json内容获取
    def download_json(self, get_pid):
        # sleep(3)
        # cookies = {
        # }
        url = 'https://aiqicha.baidu.com/detail/basicAllDataAjax?pid=' + get_pid
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # headers = {'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent, "Referer": url}
        try:
            print(url)
            # 此处可以使用json.loads(text_data)或者requests.get().json()。但由于爬取的数据不一定严格形式的json，因此可以使用eval()部分解决问题
            # 若忽略掉问题数据，可以直接try+except
            # 下同
            # text_data = requests.get(url, headers=headers, timeout=30, cookies=cookies).text
            text_data = self.dj_get_req.get_requests(url)
            # print(text_data.encode().decode('unicode_escape'))
            data = yaml.load(text_data, Loader=yaml.FullLoader)
            # 关于yaml.load()的错误问题：https://blog.csdn.net/sinat_40831240/article/details/90054108
            # 或者 data = json.loads(text_data)
            print(data)
            return data
        except Exception as e:
            os.system('chcp 65001')
            # win环境下
            # exit_code = os.system('ping www.baidu.com')
            # Linux环境下
            exit_code = os.system('ping -c 4 www.baidu.com')
            if exit_code:
                print("Connect failed in download.")
                return 'Fail'
            else:
                print("download_json Requests Error")
                return None

    def click_next(self, sign, i_page, page_size, main_pid):
        # sleep(3)
        """
        :param main_url: 当前需要点击的主页
        :param sign: 对某种企业关系的标识
        :param main_pid: 主页公司的pid
        :return:
        """
        # cookies = {
        # }
        url = ''
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 下一页的json文件，因需求不同而格式有所变化
        if sign == 'investRecord':
            url = 'https://aiqicha.baidu.com/detail/investajax?p='+str(i_page)+'&size='+str(page_size)+'&pid='+main_pid
        elif sign == 'branchs':
            url = 'https://aiqicha.baidu.com/detail/branchajax?p='+str(i_page)+'&size='+str(page_size)+'&pid='+main_pid
        elif sign == 'holds':
            url = 'https://aiqicha.baidu.com/detail/holdsAjax?pid='+main_pid+'&p='+str(i_page)+'&size='+str(page_size)
        # headers = {'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent, "Referer": url}
        try:
            print(url)
            # text_data = requests.get(url, headers=headers, timeout=30, cookies=cookies).text
            # print(text_data.encode().decode('unicode_escape'))
            text_data = self.cn_get_req.get_requests(url)
            data = yaml.load(text_data, Loader=yaml.FullLoader)
            print(data)
            return data
        except Exception as e:
            os.system('chcp 65001')
            # win环境下
            # exit_code = os.system('ping www.baidu.com')
            # Linux环境下
            exit_code = os.system('ping -c 4 www.baidu.com')
            if exit_code:
                print("Connect failed in click_next.")
                return 'Fail'
            else:
                print('click_next Requests Error')
                return None
