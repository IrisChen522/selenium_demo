# coding:utf-8
import time
from selenium import webdriver


# 启动driver
driver = webdriver.Chrome()
# 启动浏览器
driver.get("http://www.baidu.com")

# # 通过name方式定位
# driver.find_element_by_name("wd").send_keys("selenium")
# # 通过tag name方式定位
# driver.find_element_by_tag_name("input").send_keys("selenium")
# # 通过class name方式定位
# driver.find_element_by_class_name("s_ipt").send_keys("selenium")
# # 通过CSS方式定位
# driver.find_element_by_css_selector("#kw").send_keys("selenium")
# # 通过xpath方式定位
# driver.find_element_by_xpath("//input[@id='kw']").send_keys("selenium")

# 通过id方式定位
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)

# 打印当前页面title
title = driver.title
if title.find("selenium") > -1:
    print("搜索成功")

# 关闭浏览器
driver.quit()
