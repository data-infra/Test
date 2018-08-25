# 在命令行执行python test_load.py来运行
import sys
import os
BASE_PATH = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
BASE_PATH = os.path.dirname(BASE_PATH)
sys.path.append(BASE_PATH)   # 将根目录添加到系统目录,才能正常引用其他文件的内容


import unittest
from utils.config import Config, REPORT_PATH,DATA_PATH
from utils.client import Asyncio_Client
from utils.log import logger
from utils.file_reader import YamlReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode
import requests,urllib
import random
import time
import io,os
import asyncio,aiohttp

# 服务器高并发压力测试
class Test_Load(unittest.TestCase):

    config = Config()
    url = config.get('local_url')    # 集群测试
    url = config.get('api_url')      #  华为api网关测试
    print('测试网址：',url)
    images = config.get('images')     # 测试图片

    num=int(config.get('num'))
    print('测试并发量：', num)
    total_time=0  # 总耗时
    total_payload=0  # 总负载
    total_num=0  # 总并发数
    all_time=[]

    # 设置访问网址和请求方式
    def setUp(self):
        self.client = Asyncio_Client()
        print('准备工作')


    # 创建一个异步任务
    async def task_func(self):
        data = {'image_id': 2}
        begin = time.time()
        print('开始发送：', begin)
        files = {'image': open(self.image, 'rb')}  # open的目录启动命令的目录，我在server.py目录启动，所以使用的这个路径
        r = requests.post(self.url,data=data,files=files)
        print(r.text)
        end = time.time()
        self.total_time += end - begin
        print('接收完成：', end)

    # 创建一个异步任务，本地测试，所以post和接收几乎不损耗时间，可以等待完成，主要耗时为算法模块
    async def task_func1(self,session):

        begin = time.time()
        # print('开始发送：', begin)
        file=open(self.image, 'rb')
        fsize = os.path.getsize(self.image)
        self.total_payload+=fsize/(1024*1024)

        data = {"image_id": "2", 'image':file}
        r = await session.post(self.url,data=data)  #只post，不接收
        result = await r.json()
        self.total_num+=1
        # print(result)
        end = time.time()
        # print('接收完成：', end,',index=',self.total_num)
        self.all_time.append(end-begin)

    # 负载测试
    def test_safety(self):

        print('test begin')
        async_client = Asyncio_Client()  # 创建客户端

        for i in range(1000):  # 执行1000次
            session = aiohttp.ClientSession()
            try:

                self.all_time=[]
                self.total_num=0
                self.total_payload=0
                self.image = DATA_PATH + "/" + self.images[0]  # 设置测试nayizhang
                print('测试图片：', self.image)
                begin = time.time()
                async_client.set_task(self.task_func1,self.num,session)  # 设置并发任务
                async_client.run()   # 执行任务

                end=time.time()
                self.all_time.sort(reverse=True)
                # print(self.all_time)
                print('并发数量(个)：',self.total_num)
                print('总耗时(s)：',end-begin)
                print('最大时延(s)：',self.all_time[0])
                print('最小时延(s)：', self.all_time[len(self.all_time)-1])
                print('top-90%时延(s)：', self.all_time[int(len(self.all_time)*0.1)])
                print('平均耗时(s/个)：',sum(self.all_time)/self.total_num)
                print('支持并发率(个/s):',self.total_num/(end-begin))
                print('总负载(MB)：',self.total_payload)
                print('吞吐率(MB/S)：',self.total_payload/(end-begin))   # 吞吐率受上行下行带宽，服务器带宽，服务器算法性能诸多影响
            except Exception as e:
                pass
            time.sleep(1)
            session.close()
        print('test finish')



if __name__ == '__main__':
    suite = unittest.TestSuite()   # 创建测试组


    tests = [Test_Load("test_safety")]  # 添加测试用例列表
    suite.addTests(tests)  # 将测试用例列表添加到测试组中
    # 直接将结果输出到控制台
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # 将测试结果输出到测试报告
    # report = REPORT_PATH + '/report.html'
    # with open(report, 'wb') as f:
    #     runner = HTMLTestRunner(f, verbosity=2, title='华为鉴黄', description='压力测试html报告')
    #     runner.run(suite)
