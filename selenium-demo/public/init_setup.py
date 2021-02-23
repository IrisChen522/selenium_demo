# coding:utf-8
from selenium import webdriver
from common.log import TestLog
import config.global_param as global_param


def init_test__info(self):
    """初始化测试的基本配置信息"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": global_param.device_name})
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.get(global_param.app_url)
    self.test_log = TestLog.getLog()

