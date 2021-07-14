（1）安装火狐浏览器；并安装使用geckodriver：
https://blog.csdn.net/rhx_qiuzhi/article/details/80296801
（2）只有没出现过"All of the orgs are searched and writen."，重启时都是运行aiqicha_main.py：运行之前，请您把deficiency_org、upperlist、lowerlist等文件删除，再运行程序。若"All of the orgs are searched and writen."已经出现过（即，您的程序输出不再显示：正在搜索查询XXX公司），以后每次重启（无论什么原因导致的重启）都运行aiqicha_again_main.py，其他文件不做操作。
（3）少量出现"Connect failed in download_requests."、"Connect failed in search."或"Button fail"没有关系，但如果连续大量重现该字符串，请重新重新运行aiqicha_main.py。运行之前，请您把deficiency_org、upperlist、lowerlist等文件删除，再运行程序。如还有异常，请联系我。
（4）如果可以ping通，但总输出"Button fail"，那么可能是您的火狐浏览器未启动。这时，建议您使用Chrome，将SearchParser中的Firefox字符改成Chrome。
（5）出现"The html_content of parser_search is error!"、"download_json Requests Error"、'click_next Requests Error'时，说明搜索出的网页内容有误，可能是验证码等，代理IP后一般不会出现。如果少量出现，可以忽略。如果大量频繁出现，请联系我。
（6）运行本程序需要python3.5及以上版本，并安装包pyyaml、jsonpath、json、selenium；
（7）运行时的主程序是aiqicha_main.py；如果突现断网、断电等外部异常情况，请参照（2）重新运行程序。
（8）刚开始运行时，请保证至少5小时的联网（不能断网），这是因为程序搜索过程未设置断网重启机制，参照（2）.
（9）<1>不同的机器需在aiqicha_main.py的第134行name_list = name_list[eve_num*8:]处进行修改，这里设置一下每个人的次序：

    name_list = name_list[0:eve_num*2] 
    name_list = name_list[eve_num*2:eve_num*4] 
    name_list = name_list[eve_num*4:eve_num*6] 
    name_list = name_list[eve_num*6:eve_num*8] 
    name_list = name_list[eve_num*8:] 

　　<2>在Get_Requests.py里面18—23行改一下proxyHost、proxyPort、proxyUser、proxyPass4个参数，如某参数：
    proxyHost = "u6226.5.tp.16yun.cn"
    proxyPort = "6445"
    proxyUser = "16WLZRTV"
    proxyPass = "642779"
（10）如果您有事需要长时间外出，请先主动断网，等3分钟再关闭程序。这是因为程序的断网重启机制比异常重启机制恢复的更快。您归来后重启程序时，请参照（2）。
（11）输出"开始第X层的数据解析"后，输出显示字典（json）信息才算正常，否则有误请联系我。
（12）程序出现"第3层的数据解析结束"+"全部处理完毕"时，表示爬取结束。此时需要反馈数据，包括All_data和deficiency_org.
（13）字符串转成json，可以使用load()/loads()/json()/eval()，但是本代码使用了re，还是因为网站不规范，很多未知错误。
（14）该爬虫属于动态网站爬虫方法，主要是在看不到网页源码的情况下进行js和json内容的爬取。网页呈现细节，可以参考：
https://blog.csdn.net/m0_37872090/article/details/100073265?utm_term=%E5%8A%A8%E6%80%81%E7%BD%91%E9%A1%B5%E7%88%AC%E5%8F%96json%E6%96%87%E4%BB%B6&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-5-100073265&spm=3001.4430

