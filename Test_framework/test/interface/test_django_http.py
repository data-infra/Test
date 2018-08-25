import unittest
from utils.config import Config, REPORT_PATH,DATA_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.file_reader import YamlReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
import requests,urllib
import random,io,os
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0] + '/../../'
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config_django.yml')

# choicevalue=[-5,-1,0,1,5,None,"",'aaaaa','\n',3.6]
choicevalue=['wwww']

class TestDjangoHTTP(unittest.TestCase):
    config = Config(CONFIG_FILE)
    URLbase = config.get("URLbase")
    urls = config.get('urls')


    def setUp(self):
        # self.client = HTTPClient(url=self.URLbase, method='GET')
        print('准备工作')

    def test_django_http(self):
        for url1 in self.urls:
            for url2 in self.urls[url1]:
                senddata={}
                for i in range(1):
                    for key in self.urls[url1][url2]:
                        senddata[key] = random.choice(choicevalue)
                        # for randvalue in choicevalue:
                        #     senddata[key] = randvalue

                    senddata['userid']=10
                    postdata = urllib.parse.urlencode(senddata)  # urlencode()字典序列化
                    postdata = postdata.encode('utf-8')  # 将字符串编码成字节数组
                    url = self.URLbase+url1+"/"+url2
                    request = urllib.request.Request(url,data=postdata)  # 创建post请求对象，get请求对象：urllib2.Request(url+"?"+data)
                    response = urllib.request.urlopen(request)  # post请求消息
                    try:
                        back = str(response.read(),encoding='gbk')  # 读取响应数据
                        print(back)
                    except Exception as e:
                        print(url,postdata)
                        return




        # logger.debug(res.text)
        # assertHTTPCode(res, [400])
        # self.assertIn('django测试', res.text)


# if __name__ == '__main__':
#     report = REPORT_PATH + '\\report.html'
#     with open(report, 'wb') as f:
#         runner = HTMLTestRunner(f, verbosity=2, title='栾鹏全栈', description='接口html报告')
#         runner.run(TestDjangoHTTP('test_baidu_http'))
