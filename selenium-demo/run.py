# coding:utf-8
import unittest
import sys
import os
import time

import HTMLReport as HTMLReport

from common.HTMLTestRunner import HTMLTestReportCN
from test_case.test_login import LoginTestCase
from test_case.test_unittest import TestUnittest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
print(rootPath)
sys.path.append(rootPath)


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

def all_test():
    """
    创建测试集
    :return:
    """
    suite = unittest.TestSuite()
    # 运行登录测试用例的登陆case
    test_login = unittest.TestLoader().loadTestsFromTestCase(LoginTestCase)
    suite.addTests(test_login)

    test_unittest = unittest.TestLoader().loadTestsFromTestCase(TestUnittest)
    suite.addTest(test_unittest)

    return suite

if __name__ == '__main__':
    test_suites = all_test()
    # runner = unittest.TextTestRunner(verbosity=1)
    runner = HTMLReport.TestRunner(report_file_name='test',
                                   output_path='report',
                                   title='测试报告',
                                   description='测试描述',
                                   sequential_execution=True
                                   )
    runner.run(test_suites)
