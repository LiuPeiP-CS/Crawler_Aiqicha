# -*- coding:utf-8 -*-

import requests
import random
from time import sleep


class GetRequests(object):

    def __init__(self):
        # 初始化对象
        self.user_agents = []
        self.read_uas()

    def get_requests(self, url):

        # 代理服务器(产品官网 www.16yun.cn)
        proxyHost = "u6226.5.tp.16yun.cn"
        proxyPort = "6445"

        # 代理验证信息
        proxyUser = "16JNVJKT"
        proxyPass = "235938"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        cookies = {
        }

        # 设置 http和https访问都是用HTTP代理
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        # 尝试重连3次
        request_iter = 0
        while request_iter < 3:
            try:
                # 随机选择ua
                user_agent = random.choice(self.user_agents)

                #  设置IP切换头
                tunnel = random.randint(1, 10000)
                headers = {"Proxy-Tunnel": str(tunnel), 'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent,
                           "Referer": url}

                resp = requests.get(url, proxies=proxies, headers=headers, timeout=30, cookies=cookies)
                if resp.status_code == 200:
                    text_data = resp.text
                    resp.encoding = 'utf-8'
                elif resp.status_code == 429 or resp.status_code == 407:
                    request_iter = request_iter + 1
                    sleep(1)
                    continue
                else:
                    print("The status_code is error")
                resp.close()
                break
            except Exception as e:
                request_iter = request_iter + 1
                sleep(1)
        # 要么返回正常内容，要么返回异常（变量未定义，但是会在上一级调用函数处理该异常）
        return text_data

    def read_uas(self):
        content = open('user-agent.txt')
        for line in content:
            if line.strip() != '':
                self.user_agents.append(line.strip())
