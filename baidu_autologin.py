# coding: utf-8

import urllib,urllib2
import re
import cookielib
import json


TOKEN_URL = "https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&apiver=v3"
INDEX_URL = "http://www.baidu.com/"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

reg_token = re.compile("\"token\"\s+:\s+\"(\w+)\"")

Headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate,sdch",
                "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
                "Host":"passport.baidu.com",
                "Origin":"http://www.baidu.com",
                "Referer":"http://www.baidu.com/",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
             }

Data = {
            "staticpage":"https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
            "token":"",
            "tpl":"netdisk",                               #重要,需要跟TOKEN_URL中的相同
            "username":"",
            "password":"",
          }

class baidu(object):

    def __init__(self):
        self._cookie = cookielib.CookieJar()
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self._cookie))

    def login(self, user = '', pwd = ''):
        print 'User: ' + user
        print 'password: ' + pwd

        self._initial()
        self._getToken()

        Data['username'] = user
        Data['password'] = pwd
        Data['token'] = self._token

        request = urllib2.Request(LOGIN_URL, headers = Headers)
        result = self._opener.open(request, urllib.urlencode(Data).encode('utf-8'))
        result = json.loads(self._opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
        if(result["no"] == 0):
            print ("OK, login succes!")                                 #判断是否登录成功
            return self._opener
        else:
            print("WTF, there is something wrong...")
            return None

    def _getToken(self):
        self._token = reg_token.findall(str(self._opener.open(TOKEN_URL).read()))[0]

    def _initial(self):
        self._opener.open(INDEX_URL)

def main():
    robot = baidu()
    #传入用户名和密码
    for line in open("user.conf"):
        user, password = str(line).strip('\n').split(",")
        robot.login(user, password)


if __name__ == "__main__":
    main()
