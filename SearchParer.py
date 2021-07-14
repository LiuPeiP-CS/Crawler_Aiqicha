# -*- coding:utf-8 -*-
import codecs
import os
import requests
from time import sleep
from selenium import webdriver
import re
from Get_Requests import GetRequests
import random


class SearchParser(object):
    def __init__(self):
        # 初始化对象
        self.org_names_list = []
        self.sp_get_req = GetRequests()

        # 代理服务器(产品官网 www.16yun.cn)
        self.proxyHost = "u6226.5.tp.16yun.cn"
        self.proxyPort = "6445"

        # 代理验证信息
        self.proxyUser = "16JNVJKT"
        self.proxyPass = "235938"

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

        self.user_agents = []
        content = open('user-agent.txt')
        for line in content:
            if line.strip() != '':
                self.user_agents.append(line.strip())

    def search_parser(self, names):
        for eve_name in names:
            options = webdriver.FirefoxOptions()

            user_agent = random.choice(self.user_agents)
            #  设置IP切换头
            tunnel = random.randint(1, 10000)
            headers = {"Proxy-Tunnel": str(tunnel), 'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent}
            # 设置无头浏览器
            options.add_argument('--headless')
            options.add_argument('--headers = ' + str(headers))
            options.add_argument('--proxy-server = ' + self.proxyMeta)

            driver = webdriver.Firefox(options=options)
            # 设置最长请求等待时间
            driver.implicitly_wait(90)
            if len(eve_name.strip()) != 0:
                # data = None
                try:
                    print("正在搜索查询%s" % eve_name)
                    driver.get("https://aiqicha.baidu.com/")
                    # 获取爱企查的搜索框
                    input = driver.find_element_by_id("aqc-search-input")
                    # 获取搜索时的点击按钮
                    button = driver.find_element_by_xpath('//button[@class="search-btn"]')
                    # 清空搜索框的默认内容
                    input.clear()
                    # 输入新内容
                    input.send_keys(eve_name)
                    # 点击搜索按钮
                    button.click()  # 或者模拟回车 input.send_keys(Keys.RETURN)
                    sleep(5)
                    data = driver.page_source
                    """
                    # 查询后获得的新网页地址
                    new_url = driver.current_url
                    # driver.close()
                    print('搜索%s时的网络地址为: %s' % (eve_name, new_url))
                    # 搜索每家公司返回的网页内容
                    data = self.download_requests(new_url)
                    """
                except Exception as e:
                    os.system('chcp 65001')
                    # win环境下
                    # exit_code = os.system('ping www.baidu.com')
                    # Linux环境下
                    exit_code = os.system('ping -c 4 www.baidu.com')
                    if exit_code:
                        print("Connect failed in search.") # 此时程序不会断掉，但会将搜索失败的企业加入deficiency_org
                        data = 'Fail'
                    else:
                        # 浏览器启动失败
                        print("Button fail")
                        data = None
                deficiency = codecs.open('deficiency_org', 'a+', encoding='utf-8')
                if data is 'Fail' or data is None:
                    # 一般是查询超时或网络断连
                    deficiency.write(eve_name + '\n')
                else:
                    # 对网页内容进行解析，获取网页上的第一家公司(默认就是当前公司)的pid
                    new_org_pid = self.parser_search(data)
                    if new_org_pid is not None:
                        self.org_names_list.append(new_org_pid)
                    else:
                        # 网页解析不出来内容，一般是查不出来该公司
                        # print("爱企查中没有%s" % eve_name)
                        # 将无法查询的企业名称进行记录
                        deficiency.write(eve_name + '\n')
                deficiency.close()
            driver.quit()

    def download_requests(self, url):
        # cookies = {
        # }
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # headers = {'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent, "Referer": url}
        # print('download_requests  get')
        # 设置请求等待时间
        try:
            # r = requests.get(url, headers=headers, timeout=30, cookies=cookies)
            text_data = self.sp_get_req.get_requests(url)
            return text_data
        except Exception as e:
            os.system('chcp 65001')
            # win环境下
            # exit_code = os.system('ping www.baidu.com')
            # Linux环境下
            exit_code = os.system('ping -c 4 www.baidu.com')
            if exit_code:
                print("Connect failed in download_requests.")
                return 'Fail'
            else:
                print("Wrong html_content in download_requests !")
                return None

    def parser_search(self, html_cont):
        """
        :param html_cont: 下载的网页内容
        :return: 返回数据
        """
        if html_cont is None:
            return None
        else:
            try:
                text = html_cont.replace('\/', '').encode().decode('unicode_escape')
                # 正则表达式匹配出"result":与"facets":{之间的内容：因为这两个字符串在所有网页中是通用的。
                # 如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始；而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。
                # 正则表达式中的括号会把匹配结果分成若干组，其中group(X)表示提取第X组的内容
                # 正则表达式加了（）小括号之后，不仅会输出匹配的内容，还会再一次输出小括号中匹配的内容。见：https://m.imooc.com/qadetail/229445
                result = '{' + re.search('"result":{(.*?)"facets":{"', text, flags=re.S).group(1) + '}'
                result = re.sub('class=".*?"', '', result).replace('<em>', '')
                # eval用来执行字符串的表达式，并返回相关结果，其可以将字符串转换成字典。见：https://www.runoob.com/python/python-func-eval.html
                # data = eval(result)
                # pid = data['resultList'][0]['pid']
                # 选择第一个查询结果
                result = re.search('''{"pid":(.*?),"entName"''', result, flags=re.S)
                if result is not None:
                    pid = result.group(1)
                    return pid.strip('"')
                else:
                    # 匹配不出任何企业信息
                    print("There is no such company in aiqicha")
                    return None
            except Exception as e:
                print("The html_content of parser_search is error!")
                return None
