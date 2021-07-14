import jsonpath
import json
import codecs


read_file = codecs.open('/media/liupei/LIUPEI/HW_Dataset/Guoqi_All_data_Fusion', 'r', encoding='utf-8')
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
with codecs.open("/media/liupei/LIUPEI/HW_Dataset/guoqi.txt", 'r', encoding='utf8') as read_file:
    # json读出来的是dict type
    ent_infor = json.load(read_file)
    # jsonpath读取公司列表
    name_list = jsonpath.jsonpath(ent_infor, '$..name')
    print("读取json文件中的企业信息")
    print(len(name_list))
read_file.close()
'''