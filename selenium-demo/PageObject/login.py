# coding:utf-8
from common.utils_element import ElementUtils


class LoginPage:

    user_input = {'element_info': "//*[@type='text']",
                  'find_type': 'xpath',
                  'txt': '用户名文本框',
                  'operate_type': 'set_value',
                  'tag_name': 'input',
                  'value': ''}
    pwd_input = {'element_info': "//*[@type='password']",
                 'find_type': 'xpath',
                 'txt': '密码文本框',
                 'operate_type': 'set_value',
                 'tag_name': 'input',
                 'value': ''}
    btn_login = {'element_info': "//div[contains(@class,'login') and contains(@class,'wfm-btn')]",
                 'find_type': 'xpath',
                 'txt': '登录按钮',
                 'operate_type': 'click'}

    success_check = {'element_info': "notice",
                     'find_type': 'class_name',
                     'check': 'default_check',
                     'txt' : '验证是否登录成功'
                     }

    def __init__(self, driver,case_info,log):
        self.driver = driver
        self.log = log
        self.case_info = case_info
        self.ele_util = ElementUtils(self.driver)

    def iuput_user_name(self, value):
        self.user_input["value"] = value
        return self.ele_util.operate(self.user_input, self.case_info, self.log, isclear=True)

    def iuput_pwd(self, value):
        self.pwd_input["value"] = value
        return self.ele_util.operate(self.pwd_input, self.case_info, self.log, isclear=True)

    def login_click(self):
        return self.ele_util.operate(self.btn_login, self.case_info, self.log)

    def check(self, id):
        if id == '002':
            return self.ele_util.check(self.user_input, self.case_info, self.log)
        elif id == '001':
            return self.ele_util.check(self.success_check, self.case_info, self.log)
