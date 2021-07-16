# -*- coding:utf-8 -*-

import requests
from time import sleep
import jsonpath
import json
import codecs
import csv
import re
from selenium import webdriver

'''
# 该程序统计各关系的企业数量
read_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/Guoqi_All_data_Fusion', 'r', encoding='utf-8')
json_dict = json.load(read_file)
read_file.close()

invest_count = 0
branch_count = 0
hold_count = 0

for key, value in json_dict.items():
    for k,v in value.items():
        if k == "分支机构":
            branch_count = branch_count + len(v)
        elif k == "对外投资":
            invest_count = invest_count + len(v)
        elif k == "控股企业":
            hold_count = hold_count + len(v)

print("分支机构的关系数为%s" % branch_count)
print("对外投资的关系数为%s" % invest_count)
print("控股企业的关系数为%s" % hold_count)
'''

'''
# 该程序统计总共的公司数量
with codecs.open("/media/liupei/LIUPEI/HuWang/Dataset/guoqi.txt", 'r', encoding='utf8') as read_file:
    # json读出来的是dict type
    ent_infor = json.load(read_file)
    # jsonpath读取公司列表
    name_list = jsonpath.jsonpath(ent_infor, '$..name')
    print("读取json文件中的企业信息")
    print(len(name_list))
    read_file.close()
'''

'''

# 该程序统计行业内容

# 构建csv文件对象
csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/Industry_statics.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['序号', '行业类型', '央企数量', '国企数量'])

gread_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/Guoqi_All_data_Fusion', 'r', encoding='utf-8')
guoqi_orgs_dict = json.load(gread_file)
gread_file.close()

yread_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/Yangqi_All_data_Fusion', 'r', encoding='utf-8')
yangqi_orgs_dict = json.load(yread_file)
yread_file.close()

industry = [] # 此处是行业内容

# 该部分统计行业数量及输出行业信息
for org_name, org_details in guoqi_orgs_dict.items():
    for reg_inv_key, reg_inv_detail in org_details.items():
        if reg_inv_key == '工商注册':
            for reg_inf_key, reg_inf_details in reg_inv_detail.items():
                if reg_inf_key == '所属行业':
                    industry.append(reg_inf_details)
                    industry = list(set(industry))
# print(industry)
# print(len(industry))
ind_iter = 0
# 该部分统计每个行业的企业数量
for each_ind in industry:
    OrgNum_In_EachInd_G = []
    for org_name, org_details in guoqi_orgs_dict.items():
        for reg_inv_key, reg_inv_detail in org_details.items():
            if reg_inv_key == '工商注册':
                for reg_inf_key, reg_inf_details in reg_inv_detail.items():
                    if reg_inf_key == '所属行业' and reg_inf_details == each_ind: # 具体到每个行业
                        OrgNum_In_EachInd_G.append(org_name)
                        OrgNum_In_EachInd_G = list(set(OrgNum_In_EachInd_G))
                        break
                break

    OrgNum_In_EachInd_Y = []
    for org_name, org_details in yangqi_orgs_dict.items():
        for reg_inv_key, reg_inv_detail in org_details.items():
            if reg_inv_key == '工商注册':
                for reg_inf_key, reg_inf_details in reg_inv_detail.items():
                    if reg_inf_key == '所属行业' and reg_inf_details == each_ind: # 具体到每个行业
                        OrgNum_In_EachInd_Y.append(org_name)
                        OrgNum_In_EachInd_Y = list(set(OrgNum_In_EachInd_Y))
                        break
                break
    ind_iter = ind_iter + 1
    print(ind_iter, each_ind, len(OrgNum_In_EachInd_Y), len(OrgNum_In_EachInd_G)) # 每个行业下的企业数量
    csv_writer.writerow([str(ind_iter), each_ind, str(len(OrgNum_In_EachInd_Y)), str(len(OrgNum_In_EachInd_G))])

csv_file.close()

'''

'''
# 处理央企
# 构建detail_csv对象
det_csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/Details_statics.csv', 'w', encoding='utf-8')
det_csv_writer = csv.writer(det_csv_file)
det_csv_writer.writerow(['序号', '企业类型', '企业名称', '注册地址', '企业官网', '所属行业', '联系方式'])
# 构建sub_csv对象
sub_csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/Sub_statics.csv', 'w', encoding='utf-8')
sub_csv_writer = csv.writer(sub_csv_file)
sub_csv_writer.writerow(['序号', '央企名称', '下属数量', '下属代表', '控股数量', '控股代表', '投资数量', '投资代表'])

# 第一级央企
yread_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/yangqi.txt', 'r', encoding='utf-8')
up_yangqi_dict = json.load(yread_file)
up_yangqi_list = jsonpath.jsonpath(up_yangqi_dict, '$..name')
yread_file.close()
print(up_yangqi_list)

# 央企详情页
ya_read_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/Yangqi_All_data_Fusion', 'r', encoding='utf-8')
yangqiall_orgs_dict = json.load(ya_read_file)
ya_read_file.close()

org_iter = 0
for each_up_yangqi in up_yangqi_list:
    add = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..注册地址')[0]
    website = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..公司官网')[0]
    indus = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..所属行业')[0]
    invest_dict = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..对外投资')[0]
    invests = list(invest_dict.keys())
    invests_num = len(invest_dict)
    hold_dict = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..控股企业')[0]
    holds = list(hold_dict.keys())
    holds_num = len(hold_dict)
    branches = jsonpath.jsonpath(yangqiall_orgs_dict, '$..'+str(each_up_yangqi)+'..分支机构')[0]
    branches_num = len(branches)
    org_iter = org_iter + 1
    det_csv_writer.writerow([str(org_iter), '央企', str(each_up_yangqi), str(add), str(website), str(indus)])
    print("*****企业详情*****")
    print(str(org_iter), '央企', str(each_up_yangqi), str(add), str(website), str(indus))
    sub_csv_writer.writerow([str(org_iter), str(each_up_yangqi), str(branches_num), str(branches), str(holds_num),
                             str(holds), str(invests_num), str(invests)])
    print("*****企业下属*****")
    print(str(org_iter), str(each_up_yangqi), str(branches_num), str(branches), str(holds_num),
                             str(holds), str(invests_num), str(invests))

det_csv_file.close()
sub_csv_file.close()
'''

"""
# 该程序处理企业细节及下属信息

# 构建detail_csv对象
det_csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/GDetails_statics.csv', 'w', encoding='utf-8')
det_csv_writer = csv.writer(det_csv_file)
det_csv_writer.writerow(['序号', '企业类型', '企业名称', '注册地址', '企业官网', '所属行业', '联系方式'])
# 构建sub_csv对象
sub_csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/GSub_statics.csv', 'w', encoding='utf-8')
sub_csv_writer = csv.writer(sub_csv_file)
sub_csv_writer.writerow(['序号', '国企名称', '下属数量', '下属代表', '控股数量', '控股代表', '投资数量', '投资代表'])


fread_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/guoqi.txt', 'r', encoding='utf-8')
up_org_dict = json.load(fread_file)
up_org_list = jsonpath.jsonpath(up_org_dict, '$..name')
fread_file.close()

# 企业详情页
read_file = codecs.open('/media/liupei/LIUPEI/HuWang/Dataset/Guoqi_All_data_Fusion', 'r', encoding='utf-8')
all_orgs_dict = json.load(read_file)
read_file.close()

'''
all_orgs_list = up_org_list
for each_org, org_details in all_orgs_dict.items():
    if each_org in up_org_list:
        invest_dict = jsonpath.jsonpath(org_details, '$..对外投资')[0]
        invests = list(invest_dict.keys())
        all_orgs_list.extend(invests)
        hold_dict = jsonpath.jsonpath(org_details, '$..控股企业')[0]
        holds = list(hold_dict.keys())
        all_orgs_list.extend(holds)
'''

org_iter = 0
for each_org, org_details in all_orgs_dict.items():
    if each_org in up_org_list:
        print(each_org)
        add = jsonpath.jsonpath(org_details, '$..注册地址')[0]
        website = jsonpath.jsonpath(org_details, '$..公司官网')[0]
        indus = jsonpath.jsonpath(org_details, '$..所属行业')[0]
        invest_dict = jsonpath.jsonpath(org_details, '$..对外投资')[0]
        invests = list(invest_dict.keys())
        invests_num = len(invest_dict)
        hold_dict = jsonpath.jsonpath(org_details, '$..控股企业')[0]
        holds = list(hold_dict.keys())
        holds_num = len(hold_dict)
        branches = jsonpath.jsonpath(org_details, '$..分支机构')[0]
        branches_num = len(branches)
        org_iter = org_iter + 1
        det_csv_writer.writerow([str(org_iter), '国企', str(each_org), str(add), str(website), str(indus)])
        print("*****企业详情*****")
        print(str(org_iter), '国企', str(each_org), str(add), str(website), str(indus))
        sub_csv_writer.writerow([str(org_iter), str(each_org), str(branches_num), str(branches), str(holds_num),
                                 str(holds), str(invests_num), str(invests)])
        print("*****企业下属*****")
        print(str(org_iter), str(each_org), str(branches_num), str(branches), str(holds_num),
                                 str(holds), str(invests_num), str(invests))

det_csv_file.close()
sub_csv_file.close()

"""


# 该程序主要是为了添加公司的联系方式

details_read = open('/media/liupei/LIUPEI/HuWang/Dataset/GDetails_statics.csv','r')
details_reader = csv.reader(details_read)
csv_content = list(details_reader) # 将所有的内容转化成list形式

det_csv_file = open('/media/liupei/LIUPEI/HuWang/Dataset/new_GDetails_statics.csv', 'w', encoding='utf-8')
det_csv_writer = csv.writer(det_csv_file)
det_csv_writer.writerow(['序号', '企业类型', '企业名称', '注册地址', '企业官网', '所属行业', '联系方式'])


def parser_search(html_cont):
    """
    :param html_cont: 下载的网页内容
    :return: 返回数据
    """
    if html_cont is None:
        return None
    else:
        # print(html_cont)
        try:
            text = html_cont.replace('\/', '').encode().decode('unicode_escape')
            # 正则表达式匹配出"pid":"与","entName":之间的内容：因为这两个字符串在所有网页中是通用的。
            # 如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始；而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。
            # 正则表达式中的括号会把匹配结果分成若干组，其中group(X)表示提取第X组的内容
            # 正则表达式加了（）小括号之后，不仅会输出匹配的内容，还会再一次输出小括号中匹配的内容。见：https://m.imooc.com/qadetail/229445
            result = re.search('"pid":"(.*?)","entName":', text, flags=re.S).group(1) # 选择index=1的内容
            if result is not None:
                pid = result
                return pid.replace('"','').replace("'","")
            else:
                # 匹配不出任何企业信息
                print("There is no such company in aiqicha")
                return None
        except Exception as e:
            print("The html_content of parser_search is error!")
            return None


def extract_cont(content):
    email = '-'
    phone = '-'
    try:
        text = content.replace('\/', '').encode().decode('unicode_escape')
        med_email = re.search('"email":"(.*?)","telephone"', text, flags=re.S).group(1)
        if med_email is not None:
            med_email = med_email.replace('"','').replace("'","")
            email_cont = med_email.split(',')
            if len(email_cont) > 1:
                email = email_cont[0]
    except Exception as e:
        print("The email can not be parsered !")
    try:
        text = content.replace('\/', '').encode().decode('unicode_escape')
        phone = re.search('"telephone":(.*?),"phoneinfo"', text, flags=re.S).group(1)
        # phone = re.findall(r"\d+", result2) # 找出所有数字
        if phone is not None:
            phone = phone.replace('"','').replace("'","")
    except Exception as e:
        print("The cell_phone can not be parsered !")

    return email+'\n'+phone


def parser_html(pid):
    url = 'https://aiqicha.baidu.com/company_detail_' + pid
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    # print('download_requests  get')
    # 设置请求等待时间
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code == 200:
        text_data = r.text
        r.encoding = 'utf-8'
        r.close()
        cell_number = extract_cont(text_data)
        return cell_number
    else:
        return '-'
    

def get_cont(name):
    cont = '-'
    for _ in range(5): # 为了防止防止反爬导致的问题，对出错的信息重复５遍
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        # 设置最长请求等待时间
        driver.implicitly_wait(90)
        try:
            print("正在搜索查询%s" % name)
            driver.get("https://aiqicha.baidu.com/")
            # 获取爱企查的搜索框
            input = driver.find_element_by_id("aqc-search-input")
            # 获取搜索时的点击按钮
            button = driver.find_element_by_xpath('//button[@class="search-btn"]')
            # 清空搜索框的默认内容
            input.clear()
            # 输入新内容
            input.send_keys(name)
            # 点击搜索按钮
            button.click()  # 或者模拟回车 input.send_keys(Keys.RETURN)
            sleep(30)
            data = driver.page_source
        except Exception as e:
            os.system('chcp 65001')
            # win环境下
            # exit_code = os.system('ping www.baidu.com')
            # Linux环境下
            exit_code = os.system('ping -c 4 www.baidu.com')
            if exit_code:
                print("Connect failed in search.")  # 此时程序不会断掉，但会将搜索失败的企业加入deficiency_org
                data = 'Fail'
            else:
                # 浏览器启动失败
                print("Button fail")
                data = None
        if data is 'Fail' or data is None:
            # 一般是查询超时或网络断连
            sleep(10)
        else:
            # 对网页内容进行解析，获取网页上的第一家公司(默认就是当前公司)的pid
            new_org_pid = parser_search(data)
            if new_org_pid is not None:
                cont = parser_html(new_org_pid)
                break
            else:
                # 网页解析不出来内容，一般是查不出来该公司
                # print("爱企查中没有%s" % eve_name)
                # 将无法查询的企业名称进行记录
                sleep(10)
        driver.quit()
    return cont
    
    
for org_content in csv_content[1:]: # 排除表头
    org_name = org_content[2]
    cont_infor = get_cont(org_name)
    org_content.append(cont_infor)
    det_csv_writer.writerow(org_content)

details_read.close()
det_csv_file.close()
