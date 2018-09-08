import time
import os
import zipfile

from multiprocessing import Pool
import uiautomator2 as u2
from Public.Devices_new import *
# from Public.Devices import *
from Public.RunCases import RunCases
from Public.ReportPath import ReportPath

from Public.Log import Log
from Public.ReadConfig import ReadConfig
from Public.Test_data import *
import logzero
from logzero import logger
import logging




class Drivers:
    @staticmethod
    def _run_cases(run, command):
        r = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s')
        formatter = logging.Formatter('[%(asctime)s'
                                      + ' %(module)s:%(lineno)d -%(levelname)s]'
                                      + ' - %s' % run.get_device()['model']
                                      + ' - %(message)s')
        logzero.formatter(formatter)
        logzero.logfile(run.get_path() + '/' + 'client.log')
        logger.info('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        run.run(command)


    def run(self, command):
        # 根据method 获取android设备
        method = ReadConfig().get_method().strip()
        if method == 'SERVER':
            # get ATX-Server Online devices
            # devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
            print('Checking available online devices from ATX-Server...')
            devices = get_online_devices()
            print('\nThere has %s alive devices in ATX-Server' % len(devices))
        elif method == 'IP':
            # get  devices from config devices list
            print('Checking available IP devices from config... ')
            devices = get_devices()
            print('\nThere has %s  devices alive in config IP list' % len(devices))
        elif method == 'USB':
            # get  devices connected PC with USB
            print('Checking available USB devices connected on PC... ')
            devices = connect_devices()
            print('\nThere has %s  USB devices alive ' % len(devices))

        else:
            raise Exception('Config.ini method illegal:method =%s' % method)

        if not devices:
            print('There is no device found,test over.')
            return

        # # # 测试前准备
        # download_apk()  # 下载小影最新的apk

        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i]))
        print(runs)
        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, command,))
            # time.sleep(2)
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')


        # #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        # create_statistics_report(runs, title=get_apk()['apk_name'])
