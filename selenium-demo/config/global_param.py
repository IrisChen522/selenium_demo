# coding:utf-8
import os
from common.c_config_parser import CConfigParser

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# 读取配置文件
config_parser = CConfigParser()
# 当前目录的绝对路径
path = PATH('.')
config_path = os.path.join(path, "config.ini")
# 数据库server
database_server = config_parser.get_value_from_config(config_path, 'DatabaseInfo', 'server')
# 数据库用户名
database_user = config_parser.get_value_from_config(config_path, 'DatabaseInfo', 'user')
# 数据库密码
database_pwd = config_parser.get_value_from_config(config_path, 'DatabaseInfo', 'pwd')
# WFM 数据库名字
wf_db_name = config_parser.get_value_from_config(config_path, 'DatabaseInfo', 'wf_db_name')
# 设备名称
device_name = config_parser.get_value_from_config(config_path, 'DeviceInfo', 'deviceName')
# 访问站点地址
app_url = config_parser.get_value_from_config(config_path, 'APPInfo', 'url')
# 服务器地址
app_server = config_parser.get_value_from_config(config_path, 'APPInfo', 'server')
# app用户名
user_name = config_parser.get_value_from_config(config_path, 'APPInfo', 'userName')
# app密码
pwd = config_parser.get_value_from_config(config_path, 'APPInfo', 'pwd')
# 语言
language = config_parser.get_value_from_config(config_path, 'APPInfo', 'language')
# server version
server_version = config_parser.get_value_from_config(config_path, 'APPInfo', 'server_version')
is_draft = config_parser.get_value_from_config(config_path, 'APPInfo', 'is_draft')
cancel_approve = config_parser.get_value_from_config(config_path, 'APPInfo', 'cancel_approve')
approve = config_parser.get_value_from_config(config_path, 'APPInfo', 'approve')
date_format = config_parser.get_value_from_config(config_path, 'APPInfo', 'date_format')
sel_row_height = config_parser.get_value_from_config(config_path, 'APPInfo', 'sel_row_height')

timepicker_text_xpath = "%s/div[1]/a/div[2]/div[2]/span"
mtfield_text_xpath = "%s/div[2]/div[2]/input"
mtcell_text_xpath = "%s/div[2]/div[2]/span"
wfinput_text_xpath = "%s//input"
seluser_text_xpath = "%s/a[1]/div[2]/div[2]/span"

