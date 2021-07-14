# -*- coding:utf-8 -*-

import requests
import os
from selenium import webdriver


def test_request_error(url):
    # url = 'http://www.baidu.com'
    # url = 'www.baidu.com'

    cookies = {
    }
    # 实验证明，user-agent与客户主机的信息以及实际使用的浏览器无关
    user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0; Touch; MAARJS)'
    headers = {'Upgrade-Insecure-Requests': '1', 'User-Agent': user_agent, "Referer": url}

    iter = 0
    # text_data = None
    while iter < 3:
        try:
            r = requests.get(url, headers=headers, timeout=30, cookies=cookies)
            if r.status_code == 200:
                text_data = r.text
                r.encoding = 'utf-8'
                # print("status_code is right")
            else:
                print("The status_code is error")
            r.close()
            break

        except Exception as e:
            iter = iter + 1
            # print(str(e))

        '''
        except Exception as e:
            print(e)
            os.system('chcp 65001')
            exit_code = os.system('ping www.baidu.com')
            if exit_code:
                print("Connect failed.")
            else:
                print("Connection is ok, but we cannot request.")
        '''
    return text_data


if __name__ == '__main__':
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    # print("OK")
    # 设置最长请求等待时间
    driver.implicitly_wait(30)
    driver.get("https://aiqicha.baidu.com/")
    # 获取爱企查的搜索框
    input = driver.find_element_by_id("aqc-search-input")
    # 获取搜索时的点击按钮
    button = driver.find_element_by_xpath('//button[@class="search-btn"]')
    # 清空搜索框的默认内容
    input.clear()
    # 输入新内容
    input.send_keys("中国移动")
    # 点击搜索按钮
    button.click()  # 或者模拟回车 input.send_keys(Keys.RETURN)
    # sleep(2)
    # 查询后获得的新网页地址
    new_url = driver.current_url
    driver.close()

    try:
        temp_r = test_request_error(new_url)
        print(temp_r)
    except:
        print("异常可接受")
