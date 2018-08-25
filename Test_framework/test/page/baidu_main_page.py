from selenium.webdriver.common.by import By
from test.common.page import Page

# 封装的百度首页

class BaiDuMainPage(Page):
    loc_search_input = (By.ID, 'kw')
    loc_search_button = (By.ID, 'su')

    def search(self, kw):
        """搜索功能"""
        self.find_element(*self.loc_search_input).send_keys(kw)  # 寻找输入框后输入搜索内容
        self.find_element(*self.loc_search_button).click()  # 寻找搜索按钮后点击按钮
