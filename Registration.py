# coding: utf-8

import baidu_autologin
import urllib,urllib2
import re
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TIEBA_URL = "http://tieba.baidu.com"
GETLIKE_URL = "http://tieba.baidu.com/f/like/mylike"
SIGN_URL = "http://tieba.baidu.com/sign/add"

reg_likeUrl = re.compile("<a href=\"([^\"]+)\" title=\"([^\"]+)\">")
reg_getTbs = re.compile("PageData.tbs = \"(\w+)\"")

def getTbTbs(opener, url):
    return reg_getTbs.findall(opener.open(TIEBA_URL).read().decode('gbk', 'ignore'))[0]

#获取喜欢的贴吧列表
def getList(opener):
    return reg_likeUrl.findall(opener.open(GETLIKE_URL).read().decode('gbk'))

signHeaders = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER",
                "Host":"tieba.baidu.com",
                "Origin":"http://tieba.baidu.com",
                "Referer":"http://tieba.baidu.com",
              }

 #要post的表格
signData = {
            "ie":"utf-8",
            "kw":"",
            "tbs":"",
           }

class autoSign:
    def __init__(self, user = "", psw = ""):
        login = baidu_autologin.baidu()
        self._opener = login.login(user, psw)
        self.user = user

    def getList(self):
        self._likeList = getList(self._opener)


    def sign(self):
        self.getList()
        lists = []
        for url in self._likeList:
            lists.append(self._signProcess(url))
            time.sleep(2)

        for ret in lists:                            #取回结果
            print (ret)

    def _signProcess(self, url):
        signData["kw"] = url[1]
        signData["tbs"] = getTbTbs(self._opener, url[0])   #获取tbs
        signHeaders["Referer"] = signHeaders["Origin"] + url[0]
        request = urllib2.Request(SIGN_URL, headers = signHeaders)
        result = json.loads(self._opener.open(request, urllib.urlencode(signData).encode("utf-8")).read().decode("utf-8"))
        if(result["no"] == 0):           #签到成功
            return u"{0}吧签到成功,今天是第{1}个签到!".format(url[1], result["data"]["uinfo"]["user_sign_rank"])
        elif(result["no"] == 1101):      #已签过
            return u"{0}吧之前已经签到过了哦!".format(url[1])
        else:                            #出错
            return u"未知错误!" + "\n" + url + "\n" + result


def main():
    ntime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print (ntime)
    for line in open("user.conf"):
        user, password = str(line).strip('\n').split(",")
        asRobot = autoSign(user, password)          #传入用户名和密码
        asRobot.sign()

if __name__ == "__main__":
    main()