# coding:utf-8
import configparser


class CConfigParser():
    """对配置文件操作类"""

    def get_value_from_config(self, file_name, section_value, key_value):
        """从配置文件读取信息"""
        cp = configparser.RawConfigParser()
        cp.read(file_name)
        v = cp.get(section_value, key_value)
        return v

