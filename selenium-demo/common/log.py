import logging
import time
import os
from time import sleep
import threading

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Log:
    def __init__(self):
        global file_path, log_path
        file_path = PATH("../log")
        log_path = os.path.join(file_path, time.strftime('%Y%m%d', time.localtime()))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.check_count = 0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # create handler,write log
        fh = logging.FileHandler(os.path.join(log_path, "outPut.log"))
        # Define the output format of formatter handler
        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    # def getMyLogger(self):
    #     """get the logger
    #     :return:logger
    #     """
    #     return self.logger

    def build_start_line(self, case_info):
        """build the start log
        :param case_info:
        :return:
        """
        start_line = "----  " + case_info + "   " + "   " + \
                    "  ----"
        # startLine = "----  " + caseNo + "   " + "START" + "   " + \
        #             "  ----"
        self.logger.info(start_line)

    def build_end_line(self, case_info):
        """build the end log
        :param case_info:
        :return:
        """
        end_line = "----  " + case_info + "   " + "END" + "   " + \
                  "  ----"
        self.logger.info(end_line)
        self.check_count = 0

    # def writeResult(self, result):
    #     """write the case result(OK or NG)
    #     :param result:
    #     :return:
    #     """
    #     reportPath = os.path.join(log_path, "report.txt")
    #     flogging = open(reportPath, "a")
    #     try:
    #         flogging.write(result + "\n")
    #     finally:
    #         flogging.close()
    #     pass
    #
    # def resultOK(self, caseNo):
    #     self.writeResult(caseNo + ": OK")
    #
    # def resultNG(self, caseNo, reason):
    #     self.writeResult(caseNo + ": NG--" + reason)

    def check_point_ok(self, driver, case_name, check_point):
        """write the case's checkPoint(OK)
        :param driver:
        :param case_name:
        :param check_point:
        :return:
        """
        self.check_count += 1
        self.logger.info("[CheckPoint_" + str(self.check_count) + "]: " + check_point + ": OK")
        print("==用例_%s检查点成功==" % case_name)
        # take shot 默认去掉成功截图
        # self.screenshotOK(driver, caseName)

    def check_point_fail(self, driver, case_name, check_point):
        """write the case's checkPoint(FAIL)
        :param driver:
        :param case_name:
        :param check_point:
        :return:
        """
        self.check_count += 1

        self.logger.info("[CheckPoint_" + str(self.check_count) + "]: " + check_point + ": FAIL")

        # take shot
        return self.screenshot_fail(driver, case_name)

    # def screenshotOK(self, driver, caseName):
    #     """screen shot
    #     :param driver:
    #     :param caseName:
    #     :return:
    #     """
    #     screenshotPath = os.path.join(logPath, caseName)
    #     screenshotName = "CheckPoint_" + str(self.check_count) + "_OK.png"
    #
    #     # wait for animations to complete before taking screenshot
    #     sleep(1)
    #     # driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))
    #     driver.get_screenshot_as_file(os.path.join(screenshotPath + screenshotName))

    def screenshot_fail(self, driver, case_name):
        """screen shot
        :param driver:
        :param case_name:
        :return:
        """
        screenshot_path = os.path.join(log_path, case_name)
        screenshot_name = "CheckPoint_" + str(self.check_count) + "_fail.png"

        # wait for animations to complete before taking screenshot
        sleep(1)
        driver.get_screenshot_as_file(os.path.join(screenshot_path + screenshot_name))
        return os.path.join(screenshot_path + screenshot_name)

    # def screenshotERROR(self, driver, caseName):
    #     """screen shot
    #     :param driver:
    #     :param caseName:
    #     :return:
    #     """
    #     screenshotPath = os.path.join(logPath, caseName)
    #     screenshotName = "ERROR.png"
    #
    #     # wait for animations to complete before taking screenshot
    #     sleep(1)
    #     driver.get_screenshot_as_file(os.path.join(screenshotPath, screenshotName))


class TestLog:
    """
    This class is used to get log
    """

    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def getLog():
        if TestLog.log is None:
            TestLog.mutex.acquire()
            TestLog.log = Log()
            TestLog.mutex.release()

        return TestLog.log


# if __name__ == "__main__":
#     logTest = TestLog.getLog("UYT0218213002069")
#     # logger = logTest.getMyLogger()
#     logTest.build_start_line("11111111111111111111111")