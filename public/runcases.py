import os
import time
import shutil


from public.maxim_monkey import Maxim
from logzero import logger as log


class RunCases:
    def __init__(self, device):
        self.test_report_root = './TestReport'
        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        date_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        self.test_report_path = self.test_report_root + '/' + date_time + '-%s' % self.device['model']
        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

        # self.file_name = self.test_report_path + '/' + 'TestReport.html'

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run(self, command):
        # set cls.driver, it must be call before operate on any page
        driver = Maxim()
        if 'ip' in self.device:
            driver.set_driver(self.device['ip'])
        else:
            driver.set_driver(self.device['serial'])
        driver.run_monkey(command)




        # with open(self.file_name, 'wb') as file:
        #     runner = HTMLTestRunner(stream=file, title=self.device['model']+'自动化测试报告', description='用例执行情况：')
        #     runner.run(cases)
        #     file.close()

            # shutil.copyfile(self.file_name, './TestReport/TestReport.html')

