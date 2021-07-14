# -*- coding:utf-8 -*-

from JsonDownload import JsonDownload
import jsonpath
import re
import sys


class JsonParser(object):

    def __init__(self):
        # 初始化对象
        self.nextjson = JsonDownload()

    def parser_main_web(self, json_cont, pid, dict_data):

        """
        :param json_cont: 传递参数html_cont
        :param pid: 被解析的企业在爱企查的pid
        :return: 返回主页里所有的子机构，包括投资、控股、分公司
        """
        # 该公司所有投资和控股公司的pid
        sub_orgs = []
        if json_cont is None:
            print("MainJson is None")
            return []

        try:
            org_infor_dict = dict()
            attr_dict = dict()
            org_infor_dict['工商注册'] = attr_dict
            invest_dict = dict()
            org_infor_dict['对外投资'] = invest_dict
            holds_dict = dict()
            org_infor_dict['控股企业'] = holds_dict
            branchs_list = list()
            org_infor_dict['分支机构'] = branchs_list

            # 获取该网页的企业名字
            org_name = jsonpath.jsonpath(json_cont, '$..basicData.entName')
            # 说明该企业存在，只有企业才能进行下一步
            if org_name:
                dict_data[org_name[0]] = org_infor_dict

                # 获取该网页上企业的属性信息
                legalPerson = jsonpath.jsonpath(json_cont, '$..basicData.legalPerson')
                # jsonpath()可能匹配不出任何内容，因此需要判断，防止出错。下同。
                if legalPerson:
                    attr_dict['法定代表人'] = legalPerson[0]
                else:
                    attr_dict['法定代表人'] = '-'

                openStatus = jsonpath.jsonpath(json_cont, '$..basicData.openStatus')
                if openStatus:
                    attr_dict['经营状态'] = openStatus[0]
                else:
                    attr_dict['经营状态'] = '-'

                prevEntName = jsonpath.jsonpath(json_cont, '$..basicData.prevEntName[0]')
                if prevEntName:
                    attr_dict['曾用名'] = prevEntName[0]
                else:
                    attr_dict['曾用名'] = '-'

                industry = jsonpath.jsonpath(json_cont, '$..basicData.industry')
                if industry:
                    attr_dict['所属行业'] = industry[0]
                else:
                    attr_dict['所属行业'] = '-'

                org_website = jsonpath.jsonpath(json_cont, '$..basicData.website')
                if org_website:
                    attr_dict['公司官网'] = org_website[0]
                else:
                    attr_dict['公司官网'] = '-'

                org_creditID = jsonpath.jsonpath(json_cont, '$..basicData.unifiedCode')
                if org_creditID:
                    attr_dict['统一社会码'] = org_creditID[0]
                else:
                    attr_dict['统一社会码'] = '-'

                licenseNumber = jsonpath.jsonpath(json_cont, '$..basicData.licenseNumber')
                if licenseNumber:
                    attr_dict['工商注册号'] = licenseNumber[0]
                else:
                    attr_dict['工商注册号'] = '-'

                orgNo = jsonpath.jsonpath(json_cont, '$..basicData.orgNo')
                if orgNo:
                    attr_dict['组织机构代码'] = orgNo[0]
                else:
                    attr_dict['组织机构代码'] = '-'

                authority = jsonpath.jsonpath(json_cont, '$..basicData.authority')
                if authority:
                    attr_dict['登记机关'] = authority[0]
                else:
                    attr_dict['登记机关'] = '-'

                startDate = jsonpath.jsonpath(json_cont, '$..basicData.startDate')
                if startDate:
                    attr_dict['成立日期'] = startDate[0]
                else:
                    attr_dict['成立日期'] = '-'

                entType = jsonpath.jsonpath(json_cont, '$..basicData.entType')
                if entType:
                    attr_dict['企业类型'] = entType[0]
                else:
                    attr_dict['企业类型'] = '-'

                openTime = jsonpath.jsonpath(json_cont, '$..basicData.openTime')
                if openTime:
                    attr_dict['营业期限'] = openTime[0]
                else:
                    attr_dict['营业期限'] = '-'

                district = jsonpath.jsonpath(json_cont, '$..basicData.district')
                if district:
                    attr_dict['行政区划'] = district[0]
                else:
                    attr_dict['行政区划'] = '-'

                regAddr = jsonpath.jsonpath(json_cont, '$..basicData.regAddr')
                if regAddr:
                    attr_dict['注册地址'] = regAddr[0]
                else:
                    attr_dict['注册地址'] = '-'

                scope = jsonpath.jsonpath(json_cont, '$..basicData.scope')
                if scope:
                    attr_dict['经营范围'] = scope[0]
                else:
                    attr_dict['经营范围'] = '-'

                invest_pid_list, invest_page, invest_pagesize, invest_pagecount\
                    = self.parser_table(json_cont, 'investRecord', 'first', invest_dict)
                sub_orgs.extend(invest_pid_list)
                while invest_page < invest_pagecount:
                    next_invest_json_content = self.nextjson.click_next('investRecord', invest_page + 1,
                                                                        invest_pagesize,
                                                                        pid)
                    # 可能click_next()可能出现断网情况，下同
                    if next_invest_json_content is 'Fail':
                        return 'Fail'
                    # 正常请求且数据正常，下同
                    elif next_invest_json_content is not None:
                        invest_pid_list, invest_page, invest_pagesize, invest_pagecount\
                            = self.parser_table(next_invest_json_content, 'investRecord', 'next', invest_dict)
                        sub_orgs.extend(invest_pid_list)

                hold_pid_list, hold_page, hold_pagesize, hold_pagecount\
                    = self.parser_table(json_cont, 'holds', 'first', holds_dict)
                sub_orgs.extend(hold_pid_list)
                while hold_page < hold_pagecount:
                    next_hold_json_content = self.nextjson.click_next('holds', hold_page + 1, hold_pagesize, pid)
                    if next_hold_json_content is 'Fail':
                        return 'Fail'
                    elif next_hold_json_content is not None:
                        hold_pid_list, hold_page, hold_pagesize, hold_pagecount\
                            = self.parser_table(next_hold_json_content, 'holds', 'next', holds_dict)
                        sub_orgs.extend(hold_pid_list)
                    # 如果返回结果是None，则重新获取该next_page，即hold_page+1

                branch_pid_list, branch_page, branch_pagesize, branch_pagecount\
                    = self.parser_table(json_cont, 'branchs', 'first', branchs_list)
                sub_orgs.extend(branch_pid_list)
                while branch_page < branch_pagecount:
                    next_branch_json_content = self.nextjson.click_next('branchs', branch_page + 1, branch_pagesize,
                                                                        pid)
                    if next_branch_json_content is 'Fail':
                        return 'Fail'
                    elif next_branch_json_content is not None:
                        branch_pid_list, branch_page, branch_pagesize, branch_pagecount \
                            = self.parser_table(next_branch_json_content, 'branchs', 'next', branchs_list)
                        sub_orgs.extend(branch_pid_list)

                print("%s已处理完成，它的详细信息是:\n%s" % (org_name, org_infor_dict))
                return sub_orgs*1
            else:
                # 解析不出该主网页的内容
                return []

        except Exception as e:
            print(str(e))
            print("PID为%s的公司网页信息有误" % pid)
            return sub_orgs*1

    def parser_table(self, json_content, sign, next_sign, dict_or_list):
        """
        :param json_content: 获取到的json页内容
        :param sign: 标识信息，用于区分投资、控股、分支
        :return: 返回数据
        """
        pid_list = []
        names = []
        regRates = []
        proportions = []
        page = sys.maxsize
        pagesize = sys.maxsize
        pagecount = sys.maxsize
        try:
            if next_sign == 'first':
                names = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..entName')
                # print(names)
                if sign is 'investRecord':
                    regRates = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..regRate')
                    # print(regRates)
                elif sign is 'holds':
                    proportions = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..proportion')
                    # print(proportions)
                pids = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..pid')
                if pids:
                    pid_list.extend(pids)
                temp_page = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..page')
                if temp_page:
                    page = temp_page[0]
                temp_pagesize = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..size')
                if temp_pagesize:
                    pagesize = temp_pagesize[0]
                temp_pagecount = jsonpath.jsonpath(json_content, '$..' + sign + 'Data..pageCount')
                if temp_pagecount:
                    pagecount = temp_pagecount[0]
            elif next_sign == 'next':
                names = jsonpath.jsonpath(json_content, '$..entName')
                # print(names)
                if sign is 'investRecord':
                    regRates = jsonpath.jsonpath(json_content, '$..regRate')
                    # print(regRates)
                elif sign is 'holds':
                    proportions = jsonpath.jsonpath(json_content, '$..proportion')
                    # print(proportions)
                pids = jsonpath.jsonpath(json_content, '$..pid')
                if pids:
                    pid_list.extend(pids)
                temp_page = jsonpath.jsonpath(json_content, '$..page')
                if temp_page:
                    page = temp_page[0]
                temp_pagesize = jsonpath.jsonpath(json_content, '$..size')
                if temp_pagesize:
                    pagesize = temp_pagesize[0]
                temp_pagecount = jsonpath.jsonpath(json_content, '$..pageCount')
                if temp_pagecount:
                    pagecount = temp_pagecount[0]

            # 注意，python判断参数类型用的是isinstance(参数，类型)
            if names and regRates and isinstance(dict_or_list, dict):
                # print("this is regRates if")
                for eve_name, eve_regrate in zip(names, regRates):
                    dict_or_list[eve_name] = eve_regrate
            elif names and proportions and isinstance(dict_or_list, dict):
                # print("this is proportions if")
                for eve_name, eve_proportion in zip(names, proportions):
                    dict_or_list[eve_name] = str(eve_proportion) + '%'
            elif names and sign is 'branchs' and isinstance(dict_or_list, list):
                # print("this is branchs if")
                dict_or_list.extend(names)

            return pid_list*1, page, pagesize, pagecount
        except Exception as e:
            print("下一页解析有误")
            return pid_list*1, page, pagesize, pagecount
