# -*- coding:utf-8 -*-
import codecs
from JsonDownload import JsonDownload
from JsonParser import JsonParser
from SearchParer import SearchParser
import json
import jsonpath
import copy


class SpiderMan(object):
    def __init__(self):
        # 初始化对象
        self.jsonparser = JsonParser()
        self.jsondownload = JsonDownload()
        self.searchparser = SearchParser()
        self.count = 0
        self.org_pid_list = []
        self.json_dict = dict()

    def search(self, names):
        self.searchparser.search_parser(names)
        self.org_pid_list = self.searchparser.org_names_list*1
        # 以下为特殊情况使用，非泛用
        # self.org_pid_list = ["83856729490135", "31653275919633", "28688281483172", "24686712604028", "28683712028160",
        #                      "99483256617106", "24886832508718", "31497775847180", "74331893061430", "28685142969693"]
        # 刷新记录list,防止程序中间出现问题
        upper_layer_num = open("upper_list", 'w')
        upper_layer_num.write(str(1) + '\n')
        upper_layer_num.close()
        upper_layer_list = open('upper_list', 'a+')
        upper_layer_list.write(str(self.org_pid_list))
        upper_layer_list.close()
        lower_layer_list = open("lower_list", 'w')
        lower_layer_list.write(str([]))
        lower_layer_list.close()
        # 每一层写入json
        wrt_file = codecs.open('All_data', 'w', encoding='utf-8')
        json.dump(self.json_dict, wrt_file, ensure_ascii=False, indent=4)
        wrt_file.close()
        print("All of the orgs are searched and writen.")

    def crawl(self):
        # 复制列表内容
        upper_pid_list = self.org_pid_list*1
        try:
            for layer in range(1, 4):
                print("开始第%s层的数据解析" % layer)
                lower_pid_list = []
                net_discon = False
                # 设置每层的每个pid最多可以请求7次
                pid_req_times = dict()
                for each_org_pid in upper_pid_list:
                    pid_req_times[each_org_pid] = 7
                while len(upper_pid_list) > 0:
                    org_pid = upper_pid_list[0]
                    # 移除已被解析的公司url（无论是否解析成功）
                    upper_pid_list.remove(org_pid)
                    # HTML下载器下载网页全部内容
                    json_content = self.jsondownload.download(org_pid)
                    if json_content is None:
                        pid_req_times[org_pid] = pid_req_times[org_pid] - 1
                        if pid_req_times[org_pid] > 0:
                            upper_pid_list.append(org_pid)
                        else:
                            print("The html_page is wrong surely !")
                    elif json_content is 'Fail':
                        # 只有断网时(请求主页时断网)，才能重新加入该pid
                        upper_pid_list.append(org_pid)
                        net_discon = True
                        break
                    else:
                        # 解析该公司的内容，并返回其子公司pid
                        ret = self.jsonparser.parser_main_web(json_content, org_pid, self.json_dict)
                        if ret is 'Fail':
                            # 只有断网时(点击下一页时断网)，才能重新加入该pid
                            upper_pid_list.append(org_pid)
                            net_discon = True
                            break
                        else:
                            suborgs = ret*1
                            suborgs = list(set(suborgs))
                            lower_pid_list.extend(suborgs)
                            lower_pid_list = list(set(lower_pid_list))
                            self.count = self.count + 1

                # 每一层写入json
                wrt_file = codecs.open('All_data', 'w', encoding='utf-8')
                json.dump(self.json_dict, wrt_file, ensure_ascii=False, indent=4)
                wrt_file.close()

                if len(upper_pid_list) == 0:
                    print("第%s层的数据解析结束" % layer)
                    if layer == 3:
                        print("全部处理完毕")
                        break

                # 刷新记录list,防止程序中间出现问题
                upper_layer_num = open("upper_list", 'w')
                upper_layer_num.write(str(layer) + '\n')
                upper_layer_num.close()
                upper_layer_list = open('upper_list', 'a+')
                upper_layer_list.write(str(upper_pid_list))
                upper_layer_list.close()
                if layer < 3:
                    lower_layer_list = open("lower_list", 'w')
                    lower_layer_list.write(str(lower_pid_list))
                    lower_layer_list.close()

                if net_discon:
                    break

                if layer < 3:
                    # 不会出现断网的情况下，将解析出的下一层作为新的上一层
                    upper_pid_list = lower_pid_list * 1

            # 解析完成后（无论是否正常解析），输出数量
            print('目前已经获得了%s家公司的信息' % self.count)
        except Exception as e:
            print(str(e))
            print("crawler failed")


if __name__ == '__main__':

    """
    # 第一期处理
    with codecs.open("yangqi.txt", 'r', encoding='utf8') as read_file:
        # json读出来的是dict type
        ent_infor = json.load(read_file)
        # jsonpath读取公司列表
        name_list = jsonpath.jsonpath(ent_infor, '$..name')
        print("读取json文件中的企业信息")
        print(name_list)
    read_file.close()
    """

    # 第二期处理
    name_list = []
    with codecs.open('Guoqi_def', 'r', encoding='utf-8') as read_file:
        for line in read_file:
            if line.strip() != '':
                name_list.append(line.strip())

    spiderman = SpiderMan()
    spiderman.search(name_list*1)
    # print("企业名单搜索完成")
    spiderman.crawl()
