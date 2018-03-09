from selenium.webdriver.common.by import By
from test.page.baidu_main_page import BaiDuMainPage

# 封装百度结果页

class BaiDuResultPage(BaiDuMainPage):
    loc_result_links = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    @property
    def result_links(self):
        return self.find_elements(*self.loc_result_links)  # 寻找所有百度搜索到的结果
