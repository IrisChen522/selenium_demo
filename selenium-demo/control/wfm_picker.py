# # coding:utf-8
# from time import sleep
# from src.common.utils_element import ElementUtils
#
#
# class WFMPickerControlPage:
#
#     btn_completed = {
#         'element_info': " ",
#         'find_type': 'xpath',
#         'txt': '点击完成',
#         'operate_type': 'click'
#
#     }
#
#     picker_selected = {
#         'element_info': "",
#         'find_type': 'xpath',
#         'txt': '选中值',
#         'operate_type': 'get_value',
#         'tag_name': 'div'
#     }
#
#     picker_selected_brother = {
#         'element_info': "",
#         'find_type': 'xpath',
#         'txt': '选中节点的兄弟节点',
#         'operate_type': 'click'
#     }
#
#     picker_type = ""
#
#     def __init__(self, driver, case_info, log, path):
#         self.driver = driver
#         self.log = log
#         self.case_info = case_info
#         self.ele_util = ElementUtils(self.driver)
#         self.btn_completed["element_info"] = path + "//div[contains(@class,'wfm-btn-group')]/div[2]"
#         self.picker_selected["element_info"] = path + "//div[contains(@class,'picker-selected')]"
#
#     def select(self, new):
#         """
#         滑动选择
#         :param new: 目标值如 进
#         :return:
#         """
#         print(new)
#         info = "滑动选择"
#         self.log.build_start_line(self.case_info["id"] + "-" + self.case_info["desc"] + "_" + info)
#         self.select_operate(new, self.picker_selected)
#         sleep(1)
#         # 点击完成
#         self.btn_completed_click()
#
#     def select_operate(self, new, item):
#         old = self.get_picker_selected_value(item, '')
#         if old != new:
#             # 先找后面相邻的兄弟节点
#             self.picker_selected_brother["element_info"] = item["element_info"] + "/following-sibling::*"
#             self.picker_selected_brother["find_type"] = "xpaths"
#             el_lst = self.ele_util.elements_by(self.picker_selected_brother)
#             leng = len(el_lst)
#             if leng > 0:
#                 i = 0
#                 while i < leng:
#                     if old != new:
#                         self.picker_selected_brother["element_info"] = item["element_info"] + "/following-sibling::div[1]"
#                         self.picker_selected_brother["find_type"] = "xpath"
#                         self.ele_util.operate(self.picker_selected_brother, self.case_info, self.log)
#                         old = self.get_picker_selected_value(item, '')
#                     i += 1
#             # 若后面相邻的兄弟节点没找到 则向前找兄弟节点
#             if old != new:
#                 # 先找后面相邻的兄弟节点
#                 self.picker_selected_brother["element_info"] = item["element_info"] + "/preceding-sibling::*"
#                 self.picker_selected_brother["find_type"] = "xpaths"
#                 el_lst = self.ele_util.elements_by(self.picker_selected_brother)
#                 leng = len(el_lst)
#                 if leng > 0:
#                     i = 0
#                     while i < leng:
#                         if old != new:
#                             self.picker_selected_brother["element_info"] = item["element_info"] + "/preceding-sibling::div[last()]"
#                             self.picker_selected_brother["find_type"] = "xpath"
#                             self.ele_util.operate(self.picker_selected_brother, self.case_info, self.log)
#                             old = self.get_picker_selected_value(item, '')
#                         i += 1
#
#     def btn_completed_click(self):
#         self.ele_util.operate(self.btn_completed, self.case_info, self.log)
#
#     def get_picker_selected_value(self, item, defalut_value):
#         """
#         获取选中的值
#         :return:
#         """
#         result = defalut_value
#         res = self.ele_util.operate(item, self.case_info, self.log)
#         if res["result"]:
#             result = res["text"]
#         return result


# coding:utf-8
from time import sleep

from common.utils_element import ElementUtils
from config.global_param import sel_row_height


class WFMPickerControlPage:

    btn_completed = {
        'element_info': " ",
        'find_type': 'xpath',
        'txt': '点击完成',
        'operate_type': 'click'
    }

    old_div = {
        'element_info': "",
        'find_type': 'xpath',
        'txt': '当前old选中值',
        'operate_type': 'get_value',
        'tag_name': 'div'
    }

    target_div = {
        'element_info': "",
        'find_type': 'xpath',
        'txt': '目标值',
        'operate_type': 'click'
    }

    option_divs = {
        'element_info': "",
        'find_type': 'xpaths',
        'txt': '同级div列表',
        'operate_type': 'click'
    }

    parent_div = {
        'element_info': "",
        'find_type': 'xpath',
        'txt': 'div父级节点',
        'operate_type': 'click'
    }

    def __init__(self, driver, case_info, log, path):
        self.driver = driver
        self.log = log
        self.case_info = case_info
        self.path = path
        self.ele_util = ElementUtils(self.driver)
        self.btn_completed["element_info"] = path + "//div[contains(@class,'wfm-btn-group')]/div[2]"
        self.old_div["element_info"] = path + "//div[contains(@class,'picker-selected')]"
        self.option_divs["element_info"] = path + "//div[contains(@class,'picker-slot-wrapper')]/div"
        self.parent_div["element_info"] = path + "//div[contains(@class,'picker-slot-wrapper')]"

    def select(self, new):
        """
        滑动选择
        :param new: 目标值如 进
        :return:
        """
        info = "滑动选择"
        self.log.build_start_line(self.case_info["id"] + "-" + self.case_info["desc"] + "_" + info)
        self.select_operate(new)
        # 点击完成
        self.btn_completed_click()

    def select_operate(self, new):
        old = self.get_picker_selected_value(self.old_div, '')
        if old != new:
            old_ele = self.ele_util.elements_by(self.old_div)
            parent_div_ele = self.ele_util.elements_by(self.parent_div)
            option_lst = self.ele_util.elements_by(self.option_divs)
            new_indx = [index for index, value in enumerate(option_lst) if value.get_attribute('innerText').find(new) >= 0]

            self.driver.execute_script("""
                    function getComputedTranslateY(obj)
                    {
                        if(!window.getComputedStyle) return;
                        var style = getComputedStyle(obj),
                            transform = style.transform || style.webkitTransform || style.mozTransform;
                        var mat = transform.match(/^matrix3d\((.+)\)$/);
                        if(mat) return parseFloat(mat[1].split(', ')[13]);
                        mat = transform.match(/^matrix\((.+)\)$/);
                        return mat ? parseFloat(mat[1].split(', ')[5]) : 0;
                    }
    
                    old_inx = Array.prototype.slice.call(arguments[1].parentNode.children).indexOf(arguments[1]);
                    var tranY = getComputedTranslateY(arguments[0]);
                    arguments[0].style.transform = "translate(0px, " + (tranY- (arguments[2] - old_inx)*arguments[3]) + "px) translateZ(0px)"
                    """, parent_div_ele, old_ele, new_indx, int(sel_row_height))

            # 点击目标节点
            sleep(0.2)
            self.target_div[
                "element_info"] = self.path + "//div[contains(@class,'picker-slot-wrapper')]/div[contains(text(), '" + new + "')]"
            self.ele_util.operate(self.target_div, self.case_info, self.log)

    def btn_completed_click(self):
        self.ele_util.operate(self.btn_completed, self.case_info, self.log)

    def get_picker_selected_value(self, item, defalut_value):
        """
        获取选中的值
        :return:
        """
        result = defalut_value
        res = self.ele_util.operate(item, self.case_info, self.log)
        if res["result"]:
            result = res["text"]
        return result



