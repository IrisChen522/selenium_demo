# coding:utf-8
import unittest


class TestUnittest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("set UP Class ")

    def setUp(self):
        print("set up ……")

    def tearDown(self):
        print("tear down ……")

    def test_02(self):
        print("test 22")
        self.assertTrue(True, 'test 22 Fail')

    def test_03(self):
        print("test 33")

    def test_01(self):
        print("test 11")

    @unittest.skip("anyway")
    def test_04(self):
        print("test 44")

    def tt_case(self):
        print("test case")

    @classmethod
    def tearDownClass(cls):
        print("tear Down Class")

if __name__=='__main__':
    # verbosity=*：默认是1；设为0，则不输出每一个用例的执行结果；2-输出详细的执行结果
    unittest.main(verbosity = 0)