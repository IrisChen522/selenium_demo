# coding:utf-8
import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from common.enum_error import get_error
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
from common.enum_element import Element as be
from time import sleep
import os


class ElementUtils():
    """对元素处理操作类"""

    def __init__(self, driver):
        self.driver = driver

    '''
    查找元素.mOperate是字典
    operate_type：对应的操作
    element_info：元素详情
    find_type: find类型
    testInfo: 用例介绍
    logTest: 记录日志
    device: 设备名
    '''
    def operate(self, item, case_info, test_log, **para):
        res = self.find_element(item)
        if res["result"]:
            res = self.operate_by(item, case_info, test_log, **para)

        # res = self.operate_by(item, case_info, test_log, **para)

        # 记录日志
        if not res["result"]:
            # 截图
            self.screen_shot(case_info["desc"])
            m = get_error({"type": res["type"], "element_info": item["element_info"], "info": item["txt"]})
            test_log.build_start_line(
            case_info["id"] + "-" + case_info["desc"] + "-" + '[ERROR]:  ' + m)  # 记录日志

        return res

    def operate_by(self, item, case_info, test_log, **para):
        try:
            info = item.get("element_info", " ") + "-" + item.get("operate_type", " ") + str(item.get("txt", " ")) + str(item.get("value", " "))
            test_log.build_start_line(case_info["id"] + "-" + case_info["desc"] + "_" + info)  # 记录日志
            find_type = item.get("find_type", "")
            by_type = By.ID
            if find_type == be.find_element_by_xpath:
                by_type = By.XPATH
            if find_type == be.find_element_by_class_name:
                by_type = By.CLASS_NAME
            if find_type == be.find_elements_by_xpath:
                by_type = By.XPATH
            try:
                WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable((by_type, item.get("element_info"))))
            except selenium.common.exceptions.TimeoutException:
                WebDriverWait(self.driver, 20).until(
                    expected_conditions.presence_of_element_located((by_type, item.get("element_info"))))
            elements = {
                be.CLICK: lambda: self.click(item),
                be.GET_VALUE: lambda: self.get_value(item),
                be.SET_VALUE: lambda: self.set_value(item, **para),
                be.SEND_ENTER: lambda: self.send_enter(item),
                be.CLICKS: lambda: self.clicks(item),
                be.CLICK_ONE: lambda: self.click_one(item),
                be.GET_COUNT: lambda: self.get_ele_count(item)
                # be.SWIPE_DOWN: lambda: self.swipe_to_down(),
                # be.SWIPE_UP: lambda: self.swipe_to_up(),
                # be.ADB_TAP: lambda: self.adb_tap(operate, device),
                # be.GET_CONTENT_DESC: lambda: self.get_content_desc(operate),
                # be.PRESS_KEY_CODE: lambda: self.press_keycode(operate)

            }
            return elements[item.get("operate_type")]()
        except IndexError:
            # test_log.build_start_line(
            #     case_info["id"] + "_" + case_info["desc"] + "_" + item["element_info"] + "索引错误")  # 记录日志
            # print(operate["element_info"] + "索引错误")
            return {"result": False, "type": be.INDEX_ERROR}

        except selenium.common.exceptions.NoSuchElementException:
            test_log.build_start_line(
                case_info["id"] + "_" + case_info["desc"] + "_" + item[
                    "element_info"] + "页面元素不存在或没加载完成")  # 记录日志
            # print(operate["element_info"] + "页面元素不存在或没有加载完成")
            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.StaleElementReferenceException:
            # test_log.build_start_line(
            #     case_info["id"] + "_" + case_info["desc"] + "_" + item[
            #         "element_info"] + "页面元素已经变化")  # 记录日志
            # print(operate["element_info"] + "页面元素已经变化")
            return {"result": False, "type": be.STALE_ELEMENT_REFERENCE_EXCEPTION}
        except KeyError:
            # 如果key不存在，一般都是在自定义的page页面去处理了，这里直接返回为真
            return {"result": True}

    # 批量点击点击事件
    def clicks(self, item):
        t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
        ele = self.elements_by(item)

        try:
            for x in ele:
                sleep(1)
                action = ActionChains(self.driver)
                action.click(x)  # 鼠标左键点击指定的元素
                action.perform()
                action.release()
        except selenium.common.exceptions.WebDriverException:
            sleep(t)
            self.driver.execute_script("arguments[0].click();", self.elements_by(item))
        return {"result": True}

        # 点击事件

    # 点击item列表中的任意一个元素
    def click_one(self, item):
        ele = self.elements_by(item)
        try:
            for x in ele:
                sleep(0.2)
                action = ActionChains(self.driver)
                action.click(x)  # 鼠标左键点击指定的元素
                action.perform()
                action.release()
                break
        except selenium.common.exceptions.WebDriverException:
            t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
            sleep(t)
            self.driver.execute_script("arguments[0].click();", self.elements_by(item))
        return {"result": True}

    # 点击事件
    def click(self, item):
            try:
                # 点击事件的几种写法：
                # self.elements_by(item).click()
                # self.elements_by(item).send_keys(Keys.ENTER)
                # self.elements_by(item).send_keys(Keys.SPACE)
                # self.driver.execute_script("arguments[0].click();", self.elements_by(item))
                sleep(0.2)
                action = ActionChains(self.driver)
                action.click(self.elements_by(item))  # 鼠标左键点击指定的元素
                action.perform()
                action.release()
                if item.get("tag_name", '') == 'button' or item.get("tag_name", '') == 'span' or item.get("tag_name", '') == 'i':
                    self.driver.execute_script("arguments[0].click();", self.elements_by(item))
            except selenium.common.exceptions.WebDriverException:
                t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
                sleep(t)
                self.driver.execute_script("arguments[0].click();", self.elements_by(item))
            return {"result": True}

    def send_enter(self, item):
        try:
            self.elements_by(item).send_keys(Keys.ENTER)
        except selenium.common.exceptions.WebDriverException:
            t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
            sleep(t)
            self.elements_by(item).send_keys(Keys.ENTER)
        return {"result": True}

    def set_value(self, item, **para):
        """
        输入值，代替过时的send_keys
        :param operate:
        :return:
        """
        ele = self.elements_by(item)
        v = item.get("value", " ")
        t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
        if item.get("tag_name", '') == 'input':
            if para['isclear']:
                txt = ele.get_attribute('value')
                try:
                    ele.click()
                except selenium.common.exceptions.WebDriverException:
                    sleep(t)
                    self.driver.execute_script("arguments[0].click();", self.elements_by(item))
                except selenium.common.exceptions.StaleElementReferenceException:
                    sleep(t)
                    self.elements_by(item).click()
                ele.clear()
                for i in range(0, len(txt)+1):
                    # 退格删除
                    ele.send_keys(Keys.BACKSPACE)

            # 方法1
            # action = ActionChains(self.driver)
            # action.send_keys_to_element(self.elements_by(item), v)  # 鼠标左键点击指定的元素
            # action.perform()
            # action.release()
            # 方法2
            self.elements_by(item).send_keys(item.get("value", " "))
            # self.driver.execute_script("arguments[0].value='" + v + "';", self.elements_by(item))
            # 方法3、
            # pyperclip.copy("http://10.10.88.54/Platinumworkforce")
            # self.elements_by(item).click()  # 点击一下百度的输入框
            # time.sleep(0.5)
            # k = PyKeyboard()
            # # 模拟键盘点击ctrl+v
            # k.press_key(k.control_key)
            # k.tap_key('v')
            # k.release_key(k.control_key)
            # self.elements_by(item).send_keys(Keys.CONTROL, 'v')
            # self.elements_by(item).click()
            # time.sleep(1)
        elif item.get("tag_name", '') == 'span':
            self.driver.execute_script("arguments[0].innerText='"+v+"';", self.elements_by(item))
        elif item.get("tag_name", '') == 'div':
            self.driver.execute_script("arguments[0].innerHTML='"+v+"';", self.elements_by(item))
        else:
            self.elements_by(item).clear()
            self.elements_by(item).send_keys(v)
        return {"result": True}

    def get_value(self, item):
        '''
        读取element的值,支持webview下获取值
        :param mOperate:
        :return:
        '''
        element_info = self.elements_by(item)
        if item.get("tag_name", '') == 'div' or item.get("tag_name", '') == 'span' or item.get("tag_name", '') == 'p':
            txt = element_info.get_attribute('innerText')
            return {"result": True, "text": txt}
        if item.get("tag_name", '') == 'input':
            txt = element_info.get_attribute('value')
            return {"result": True, "text": txt}

    def find_element(self, item):
        '''
        查找元素.mOperate,dict|list
        operate_type：对应的操作
        element_info：元素详情
        find_type: find类型
        '''
        try:
            t = item["sleep_time"] if item.get("sleep_time", "0") != "0" else be.WAIT_TIME
            WebDriverWait(self.driver, t).until(lambda x: self.elements_by(item))
            return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            # print("==查找元素超时==")
            return {"result": False, "type": be.TIME_OUT}
        except selenium.common.exceptions.NoSuchElementException:
            # print("==查找元素不存在==")
            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.WebDriverException:
            # print("WebDriver出现问题了")
            return {"result": False, "type": be.WEB_DROVER_EXCEPTION}

    # 封装常用的标签
    def elements_by(self, item):
        elements = {
            be.find_element_by_id: lambda: self.driver.find_element_by_id(item["element_info"]),
            be.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(item["element_info"]),
            be.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(item['element_info']),
            be.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(item['element_info']),
            be.find_elements_by_id: lambda: self.driver.find_elements_by_id(item['element_info']),
            be.find_elements_by_xpath: lambda: self.driver.find_elements_by_xpath(item["element_info"])
        }
        return elements[item["find_type"]]()

    def check(self, item, case_info, test_log):
        result = True
        if item.get("check", be.DEFAULT_CHECK) == be.TOAST:
            pass
            # result = \
            #     self.operate_element.toast(item["element_info"], case_info=self.case_info,
            #                                test_log=self.test_log)[
            #         "result"]
            # if result is False:
            #     m = get_error(
            #         {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["info"]})
            #     self.msg = m_s_g + m
            #     print(m)
            #     self.case_info[0]["msg"] = m
        else:
            resp = self.operate(item, case_info, test_log)
        if item.get("check", be.DEFAULT_CHECK) == be.DEFAULT_CHECK and not resp["result"]:
            m = get_error(
                {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["txt"]})
            result = False
        if item.get("check", be.DEFAULT_CHECK) == be.CONTRARY and resp["result"]:
            m = get_error({"type": be.CONTRARY, "element_info": item["element_info"], "info": item["txt"]})
            result = False
        # 检查点关键字contrary_getval: 相反值检查点，如果对比成功，说明失败
        # if item.get("check", be.DEFAULT_CHECK) == be.CONTRARY_GETVAL and self.is_get and resp["result"] \
        #         in self.get_value:
        #     m = get_error(
        #         {"type": be.CONTRARY_GETVAL, "current": item["element_info"], "history": resp["text"]})
        #     # self.msg = m_s_g + m
        #     # print(m)
        #     # self.case_info[0]["msg"] = m
        #     result = False
        if item.get("check", be.DEFAULT_CHECK) == be.COMPARE :
            if item.get("value_type", "") == "time":
                val_show = resp.get("text", "")
                val_tar = str(item.get('target_value'))
                val_show = datetime.datetime.strptime(val_show, '%H:%M')
                val_tar = datetime.datetime.strptime(val_tar, '%H:%M')
                if val_show != val_tar:
                    result = False
                    m = get_error({"type": be.COMPARE, "target": item.get('target_value', ''), "current": resp["text"]})
            else:
                if resp["text"] != str(item.get('target_value')):
                    result = False
                    m = get_error({"type": be.COMPARE, "target": item.get('target_value',''), "current": resp["text"]})
        if not result:
            test_log.build_start_line(
                 case_info["id"] + "-" + case_info["desc"] + "-" + '[Fail]:  ' + m)  # 记录日志
        # 截图
        self.screen_shot(case_info["desc"])
        return result

    # 截图
    def screen_shot(self, desc):
        PATH = lambda p: os.path.abspath(
            os.path.join(os.path.dirname(__file__), p)
        )
        file_path = PATH("../screenshot")
        log_path = os.path.join(file_path, datetime.datetime.now().strftime('%Y-%m-%d'))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        picture_time = datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
        pic_path = log_path + '\\' + picture_time + '_' + desc + '.png'
        self.driver.get_screenshot_as_file(pic_path)

    # 获取元素个数
    def get_ele_count(self, item):
        ele = self.elements_by(item)
        return {"result": True, "count": len(ele)}

    #以下暂时注释



    # # code 事件
    # def press_keycode(self, mOperate):
    #     self.driver.press_keycode(mOperate.get("code", 0))
    #     return {"result": True}

    # # 获取到元素到坐标点击，主要解决浮动层遮档无法触发driver.click的问题
    # def adb_tap(self, mOperate, device):
    #
    #     bounds = self.elements_by(mOperate).location
    #     x = str(bounds["x"])
    #     y = str(bounds["y"])
    #
    #     cmd = "adb -s " + device + " shell input tap " + x + " " + y
    #     print(cmd)
    #     os.system(cmd)
    #
    #     return {"result": True}
    #
    # def toast(self, xpath, logTest, case_info):
    #     logTest.build_start_line(case_info[0]["id"] + "_" + case_info[0]["title"] + "_" + "查找弹窗元素_" + xpath)  # 记录日志
    #     try:
    #         WebDriverWait(self.driver, 10, 0.5).until(
    #             expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    #         return {"result": True}
    #     except selenium.common.exceptions.TimeoutException:
    #         return {"result": False}
    #     except selenium.common.exceptions.NoSuchElementException:
    #         return {"result": False}
    #
    # def get_content_desc(self, mOperate):
    #     result = self.elements_by(mOperate).get_attribute("contentDescription")
    #     re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
    #     return {"result": True, "text": "".join(re_reulst)}
    #
    # '''
    # 切换native
    #
    # '''
    #
    # def switch_to_native(self):
    #     self.driver.switch_to.context("NATIVE_APP")  # 切换到native
    #
    # '''
    # 切换webview
    # '''
    #
    # # def switch_to_webview(self):
    # #     try:
    # #         n = 1
    # #         while n < 10:
    # #             time.sleep(3)
    # #             n = n + 1
    # #             print(self.driver.contexts)
    # #             for cons in self.driver.contexts:
    # #                 if cons.lower().startswith("webview_com"):
    # #                     self.driver.switch_to.context(cons)
    # #                     # print(self.driver.page_source)
    # #                     self.driver.execute_script('document.querySelectorAll("html")[0].style.display="block"')
    # #                     self.driver.execute_script('document.querySelectorAll("head")[0].style.display="block"')
    # #                     self.driver.execute_script('document.querySelectorAll("title")[0].style.display="block"')
    # #                     print("切换webview成功")
    # #                     return {"result": True}
    # #         return {"result": False}
    # #     except appium.common.exceptions.NoSuchContextException:
    # #         print("切换webview失败")
    # #         return {"result": False, "text": "appium.common.exceptions.NoSuchContextException异常"}
    #
    # # 左滑动
    # def swipe_to_left(self):
    #     width = self.driver.get_window_size()["width"]
    #     height = self.driver.get_window_size()["height"]
    #     x1 = int(width * 0.75)
    #     y1 = int(height * 0.5)
    #     x2 = int(width * 0.05)
    #     self.driver(x1, y1, x2, y1, 600)
    #     return {"result": True}
    #
    # # swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000 从200滑动到400
    # def swipe_to_down(self):
    #     height = self.driver.get_window_size()["height"]
    #     x1 = int(self.driver.get_window_size()["width"] * 0.5)
    #     y1 = int(height * 0.25)
    #     y2 = int(height * 0.75)
    #
    #     self.driver.swipe(x1, y1, x1, y2, 1000)
    #     # self.driver.swipe(0, 1327, 500, 900, 1000)
    #     print("--swipeToDown--")
    #     return {"result": True}
    #
    # def swipe_to_up(self):
    #     height = self.driver.get_window_size()["height"]
    #     width = self.driver.get_window_size()["width"]
    #     self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
    #     print("执行上拉")
    #     return {"result": True}
    #     # for i in range(n):
    #     #     self.driver.swipe(540, 800, 540, 560, 0)
    #     #     time.sleep(2)
    #
    # def swipe_to_right(self):
    #     height = self.driver.get_window_size()["height"]
    #     width = self.driver.get_window_size()["width"]
    #     x1 = int(width * 0.05)
    #     y1 = int(height * 0.5)
    #     x2 = int(width * 0.75)
    #     self.driver.swipe(x1, y1, x1, x2, 1000)
    #     # self.driver.swipe(0, 1327, 500, 900, 1000)
    #     print("--swipeToUp--")
    #     return {"result": True}
    #
    # def click_windows(self, device):
    #     try:
    #         button0 = 'com.huawei.systemmanager:id/btn_allow'
    #         # button1 = 'com.android.packageinstaller:id/btn_allow_once'
    #         # button2 = 'com.android.packageinstaller:id/bottom_button_two'
    #         # button3 = 'com.android.packageinstaller:id/btn_continue_install'
    #         # button4 = 'android:id/button1'
    #         # button5 = 'vivo:id/vivo_adb_install_ok_button'
    #         button_list = [button0]
    #         for elem in button_list:
    #             find = self.driver.find_element_by_id(elem)
    #             WebDriverWait(self.driver, 1).until(lambda x: self.elements_by(find(elem)))
    #             bounds = find.location
    #             x = str(bounds["x"])
    #             y = str(bounds["y"])
    #             cmd = "adb -s " + device + " shell input tap " + x + " " + y
    #             print(cmd)
    #             os.system(cmd)
    #             print("==点击授权弹框_%s==" % elem)
    #     except selenium.common.exceptions.TimeoutException:
    #         # print("==查找元素超时==")
    #         pass
    #     except selenium.common.exceptions.NoSuchElementException:
    #         # print("==查找元素不存在==")
    #         pass
    #     except selenium.common.exceptions.WebDriverException:
    #         # print("WebDriver出现问题了")
    #         pass
    #
    # def drag_and_drop_ele(self, start, end):
    #     actions = ActionChains(self.driver)
    #     # actions.drag_and_drop(start, end)
    #     actions.drag_and_drop_by_offset(start, 0, 36 * 9)
    #
    #     # 执行
    #     actions.perform()

