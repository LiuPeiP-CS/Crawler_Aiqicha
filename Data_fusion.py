import codecs
import jsonpath
import json

if __name__ == '__main__':
    guoqi_add = "D:/aiqicha_crawl/Dataset/Guoqi_data/Guoqi_"
    guoqi_alldata_dict = dict()
    for i in range(1, 6):
        print(i)
        file_read = open(guoqi_add + str(i), 'r', encoding='utf-8')
        local_dict = json.load(file_read)
        guoqi_alldata_dict.update(local_dict)
        file_read.close()

    guoqi_alldata_wrt = open("D:/aiqicha_crawl/Dataset/Guoqi_data/Guoqi_All_data_Fusion_1", 'w', encoding='utf-8')
    json.dump(guoqi_alldata_dict, guoqi_alldata_wrt, ensure_ascii=False, indent=4)
    guoqi_alldata_wrt.close()
    print("国企一期数据量为%s" % len(guoqi_alldata_dict.items()))

    guoqi_deficiency_add = "D:/aiqicha_crawl/Dataset/Guoqi_data/Guoqi_deficiency_"
    def_list = []
    for i in range(1, 6):
        print(i)
        def_file_read = open(guoqi_deficiency_add + str(i), 'r', encoding='utf-8')
        for def_line in def_file_read:
            if def_line.strip() != "":
                def_list.append(def_line.strip())
        def_file_read.close()
    print("国企一期缺失的数量为%s" % len(def_list))

    def_all = open("D:/aiqicha_crawl/Dataset/Guoqi_data/Guoqi_def_all", 'w', encoding='utf-8')
    for eve_str in def_list:
        def_all.write(eve_str + '\n')
    def_all.close()
    print("国企缺失数据整合完成")

    yangqi_count_read = open("D:/aiqicha_crawl/Dataset/Yangqi_data/Yangqi_1", 'r', encoding='utf-8')
    yangqi_count_dict = json.load(yangqi_count_read)
    yangqi_count_read.close()
    print("央企一期数据量为%s" % len(yangqi_count_dict.items()))




