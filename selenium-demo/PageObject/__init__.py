# coding:utf-8
from time import sleep

from common.utils_element import ElementUtils
from config import global_param
from control.wfm_picker import WFMPickerControlPage


def set_app_server(self, case_info):
    """设置服务器"""
    btn_skip = {'element_info': "//div[contains(@class,'active')]//div[contains(@class,'skip')]",
                 'find_type': 'xpath',
                 'txt': '跳过',
                 'operate_type': 'click'}
    btn_set = {'element_info': "//img[contains(@class,'wf-setting-btn')]",
                 'find_type': 'xpath',
                 'txt': '设置服务器',
                 'operate_type': 'click'}
    input_server ={'element_info': "//div[contains(@class,'wf-left-shift')]/div[2]//input",
                  'find_type': 'xpath',
                  'txt': '服务器文本框',
                  'operate_type': 'set_value',
                  'tag_name': 'input',
                  'value': global_param.app_server}

    language_href = {'element_info': "//div[contains(@class,'wf-left-shift')]/div[3]/div[1]",
                      'find_type': 'xpath',
                      'txt': '选择语言',
                      'operate_type': 'click'}

    btn_save = {'element_info': "//div[contains(@class,'wfm-setting-button')]",
                 'find_type': 'xpath',
                 'txt': '保存配置信息',
                 'operate_type': 'click'}
    ele_util = ElementUtils(self.driver)
    temp1 = ele_util.operate(btn_skip, case_info, self.test_log)
    # 点击设置
    temp2 = ele_util.operate(btn_set, case_info, self.test_log)
    # 输入服务器地址
    temp3 = ele_util.operate(input_server, case_info, self.test_log, isclear=True)
    # 选择语言
    ele_util.operate(language_href, case_info, self.test_log)
    wfm_picker = WFMPickerControlPage(self.driver,case_info,self.test_log, "//div[contains(@class,'wf-left-shift')]/div[3]")
    lan = '简体中文'
    if global_param.language == 'chinese':
        lan = '简体中文'
    elif global_param.language == 'english':
        lan = 'English'
    elif global_param.language == 'traditional':
        lan = '繁體中文'
    wfm_picker.select(lan)
    # 点击保存
    temp4 = ele_util.operate(btn_save, case_info, self.test_log)
    return (temp1["result"] and temp2["result"] and temp3["result"] and temp4["result"])


def log_out(self, case_info):
    """默认当前页在首页"""
    home_page = {'element_info': "//*[contains(@class,'icon-shouye')]",
                 'find_type': 'xpath',
                 'txt': '首页',
                 'operate_type': 'click'}
    user_info = {'element_info': "avatar",
                 'find_type': 'class_name',
                 'txt': '我',
                 'operate_type': 'click'}
    btn_log_out = {'element_info': "//div[contains(@class,'wfm-btn-wrap')]/div",
                     'find_type': 'xpath',
                     'txt': '退出登录按钮',
                     'tag_name': 'button',
                     'operate_type': 'click'}
    ele_util = ElementUtils(self.driver)
    # 点击首页
    ele_util.operate(home_page, case_info, self.test_log)
    # 点击我
    ele_util.operate(user_info, case_info, self.test_log)
    # 点击退出登录
    ele_util.operate(btn_log_out, case_info, self.test_log)


def log_in(self, case_info, use_name, pwd):
    """登录"""
    user_input = {'element_info': "//input[@type='text']",
                  'find_type': 'xpath',
                  'txt': '用户名文本框',
                  'operate_type': 'set_value',
                  'tag_name': 'input',
                  'value': use_name}
    pwd_input = {'element_info': "//*[@type='password']",
                 'find_type': 'xpath',
                 'txt': '密码文本框',
                 'operate_type': 'set_value',
                 'tag_name': 'input',
                 'value': pwd}
    btn_login = {'element_info': "//div[contains(@class,'login') and contains(@class,'wfm-btn')]",
                 'find_type': 'xpath',
                 'txt': '登录按钮',
                 'operate_type': 'click'
                 }

    success_check = {'element_info': "notice",
                     'find_type': 'class_name',
                     'check': 'default_check',
                     'txt': '验证是否登录成功'
                     }

    ele_util = ElementUtils(self.driver)
    self.driver.implicitly_wait(5)
    # 输入用户名
    ele_util.operate(user_input, case_info, self.test_log, isclear=True)
    # 输入密码
    ele_util.operate(pwd_input, case_info, self.test_log, isclear=True)
    # 点击登录
    ele_util.operate(btn_login, case_info, self.test_log)

    # 验证是否登录成功
    return ele_util.check(success_check, case_info, self.test_log)


def is_error_code_show(self, case_info):
    # undefined_check = {'element_info': "//*[contains(text(),'undefined')]",
    #                  'find_type': 'xpath',
    #                  'check': 'default_check',
    #                  'txt': '验证是否有undefined乱码'
    #                  }
    #
    ele_util = ElementUtils(self.driver)
    # #验证是否有undefined乱码
    # return ele_util.check(undefined_check, case_info, self.test_log)
    sleep(0.2)
    ele_util.screen_shot(case_info["desc"])
    return False
