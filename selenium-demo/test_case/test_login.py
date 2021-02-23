# coding:utf-8
import unittest
from time import sleep

import ddt as ddt
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from PageObject import set_app_server
from public.init_setup import init_test__info
from common.utils_excel import ExcelUtils
import sys
from PageObject.login import LoginPage


@ddt.ddt
class LoginTestCase(unittest.TestCase):
    excel_utils = ExcelUtils("login.xlsx", "test_login")
    login_data = excel_utils.dict_data()

    def setUp(self):
        init_test__info(self)

    @ddt.data(*login_data)
    def test_001_login(self, data):
        print('test_001_login')
        if data["skip"] == 'true':
            self.skipTest("强制跳过示例")
        self._testMethodDoc = data["id"] + "_" + data["case_desc"]
        case_info = {'id': sys._getframe().f_code.co_name + "_" + data["id"], 'desc': data["case_desc"]}
        isset = set_app_server(self, case_info)
        self.assertTrue(isset, '设置服务地址失败')
        # 读取用例数据
        user_name = data["user_name"]
        pwd = data["pwd"]

        login_page = LoginPage(self.driver, case_info, self.test_log)
        # # 输入用户名
        # login_page.iuput_user_name(user_name)
        # # 输入密码
        # login_page.iuput_pwd(pwd)
        # # 点击登录
        # login_page.login_click()


        WebDriverWait(self.driver, 20).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//*[@type='text']")))
        # 找到用户文本框
        input_user = self.driver.find_element_by_xpath("//*[@type='text']")
        # 输入用户名
        input_user.send_keys(user_name)

        # 找到密码框
        input_pwd = self.driver.find_element_by_xpath("//*[@type='password']")
        # 输入密码
        input_pwd.send_keys(pwd)

        # 找到登录按钮
        btn_login = self.driver.find_element_by_xpath("//div[contains(@class,'login') and contains(@class,'wfm-btn')]")
        # 点击
        btn_login.click()


        # 验证
        issuccess = login_page.check(data["id"])
        self.assertTrue(issuccess, '登录失败')

    def tearDown(self):
        driver = self.driver
        # 关闭浏览器窗口
        driver.quit()

if __name__ == '__main__':
     unittest.main()
