"""
在这里添加各种自定义的断言（测试结果和目标结果是否一致的判断），断言失败抛出AssertionError就OK。
"""

# 判断http的响应码和预期状态码是否一致
def assertHTTPCode(response, code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        raise AssertionError('响应code不在列表中！')  # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error
