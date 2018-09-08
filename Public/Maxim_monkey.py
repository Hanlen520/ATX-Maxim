#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uiautomator2 as u2
from logzero import logger
import time


# 参考网站：
# Maxim-高速 Android Monkey 工具使用记录： https://testerhome.com/topics/11884
# 基于 Android Monkey 二次开发，实现高速点击的 Android Monkey 自动化工具 fastmonkey ：https://testerhome.com/topics/11719

class Maxim(object):
    @classmethod
    def set_driver(cls, dri):
        cls.d = u2.connect(dri)

    def get_driver(self):
        return self.d

    def command(self, package, runtime, mode=None, whitelist=False, throttle=None, options=None, off_line=True):
        '''
        monkey命令封装
        :param package:被测app的包名
        :param runtime: 运行时间 minutes分钟
        :param mode: 运行模式
            uiautomatormix(混合模式,70%控件解析随机点击，其余30%按原Monkey事件概率分布)、
            pct-uiautomatormix n ：可自定义混合模式中控件解析事件概率 n=1-100
            uiautomatordfs：DFS深度遍历算法（优化版）（注 Android5不支持dfs）(u2和dsf冲突 无法使用）
            uiautomatortroy：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
            None: 默认原生 monkey
        :param whitelist: activity白名单  需要将awl.strings 配置正确
        :param throttle: 在事件之间插入固定的时间（毫秒）延迟
        :param options: 其他参数及用法同原始Monkey
        :param off_line: 是否脱机运行 默认Ture
        :return: shell命令
        '''
        classpath = 'CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey'
        package = ' -p ' + package
        runtime = ' --running-minutes ' + str(runtime)
        if mode:
            mode = ' --' + mode
        else:
            mode = ''
        if throttle:
            throttle = ' --throttle ' + str(throttle)
        else:
            throttle = ''
        if options:
            options = ' ' + options
        else:
            options = ''
        if whitelist:
            whitelist = ' --act-whitelist-file /sdcard/awl.strings'
        else:
            whitelist = ''

        off_line_cmd = ' >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &'
        if off_line:
            monkey_shell = (
                ''.join([classpath, package, runtime, mode, whitelist, throttle, options, off_line_cmd]))
        else:
            monkey_shell = (
                ''.join([classpath, package, runtime, mode, whitelist, throttle, options]))

        return monkey_shell

    #  Maxim 文件夹说明：
    # awl.strings：存放activity白名单
    # max.xpath.actions：特殊事件序列
    # max.xpath.selector：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
    # max.widget.black：黑控件 黑区域屏蔽
    # max.strings 随机输入字符，内容可自定义配置

    @classmethod
    def run_monkey(cls, monkey_shell, actions=False, widget_black=False):
        '''
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        :param monkey_shell: shell命令 uiautomatortroy 时 max.xpath.selector文件需要配置正确
        :param actions: 特殊事件序列 max.xpath.actions文件需要配置正确
        :param widget_black: 黑控件 黑区域屏蔽 max.widget.black文件需要配置正确
        :return:
        '''
        cls.clear_env()
        cls.push_jar()
        if monkey_shell.find('awl.strings'):
            cls.push_white_list()
        if monkey_shell.find('uiautomatortroy'):
            cls.push_selector()
        if actions:
            cls.push_actions()
        if widget_black:
            cls.push_widget_black()
        cls.set_AdbIME()

        runtime = monkey_shell.split('running-minutes ')[1].split(' ')[0]
        logger.info('starting run monkey')
        logger.info('It will be take about %s minutes,please be patient ...........................' % runtime)
        cls.d.shell(monkey_shell)
        time.sleep(int(runtime) * 60 + 30)
        logger.info('Maxim monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    @classmethod
    def push_jar(cls):
        cls.d.push('./Maxim/monkey.jar', '/sdcard/')
        cls.d.push('./Maxim/framework.jar', '/sdcard/')
        logger.info('push jar file--->monkey.jar framework.jar')

    @classmethod
    def push_white_list(cls):
        cls.d.push('./Maxim/awl.strings', '/sdcard/')
        logger.info('push white_list file---> awl.strings ')

    @classmethod
    def push_actions(cls):
        cls.d.push('./Maxim/max.xpath.actions', '/sdcard/')
        logger.info('push actions file---> max.xpath.actions ')

    @classmethod
    def push_selector(cls):
        cls.d.push('./Maxim/max.xpath.selector', '/sdcard/')
        logger.info('push selector file---> max.xpath.selector ')

    @classmethod
    def push_widget_black(cls):
        cls.d.push('./Maxim/max.widget.black', '/sdcard/')
        logger.info('push widget_black file---> max.widget.black ')

    @classmethod
    def push_string(cls):
        cls.d.push('./Maxim/max.strings', '/sdcard/')
        logger.info('push string file---> max.strings ')

    @classmethod
    def clear_env(cls):
        logger.info('Clearing monkey env')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        cls.d.shell('rm -r /sdcard/max.widget.black')
        cls.d.shell('rm -r /sdcard/max.xpath.selector')
        cls.d.shell('rm -r /sdcard/max.xpath.actions')
        cls.d.shell('rm -r /sdcard/awl.strings')
        cls.d.shell('rm -r /sdcard/monkey.jar')
        cls.d.shell('rm -r /sdcard/framework.jar')
        cls.d.shell('rm -r /sdcard/max.strings')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        logger.info('Clear monkey env success')

    @classmethod
    def set_AdbIME(cls):
        ime = cls.d.shell('ime list -s').output
        print(ime)
        if 'adbkeyboard' in ime:
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
            logger.info('Set adbkeyboard as default')
        else:
            cls.local_install('../apk/ADBKeyBoard.apk')
            cls.d.shell('ime enable com.android.adbkeyboard/.AdbIME')
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
            logger.info('install adbkeyboard and set as default')
        cls.push_string()

    @classmethod
    def local_install(cls, apk_path):
        '''
        安装本地apk 覆盖安装，不需要usb链接
        :param apk_path: apk文件本地路径
        '''
        file_name = os.path.basename(apk_path)
        dst = '/sdcard/' + file_name
        print('pushing %s to device' % file_name)
        cls.d.push(apk_path, dst)
        print('start install %s' % dst)
        if cls.d.device_info['brand'] == 'vivo':
            '''Vivo 手机通过打开文件管理 安装app'''
            with cls.d.session("com.android.filemanager") as s:
                s(resourceId="com.android.filemanager:id/allfiles").click()
                s(resourceId="com.android.filemanager:id/file_listView").scroll.to(textContains=file_name)
                s(textContains=file_name).click()
                s(resourceId="com.android.packageinstaller:id/continue_button").click()
                s(resourceId="com.android.packageinstaller:id/ok_button").click()
                print(s(resourceId="com.android.packageinstaller:id/checked_result").get_text())

        elif cls.d.device_info['brand'] == 'OPPO':
            with cls.d.session("com.coloros.filemanager") as s:
                s(resourceId="com.coloros.filemanager:id/action_file_browser").click()
                s(className="android.app.ActionBar$Tab", instance=1).click()
                s(resourceId="com.coloros.filemanager:id/viewPager").scroll.to(textContains=file_name)
                s(textContains=file_name).click()

                btn_done = cls.d(className="android.widget.Button", text=u"完成")
                while not btn_done.exists:
                    s(text="继续安装旧版本").click_exists()
                    s(text="重新安装").click_exists()
                    # 自动清除安装包和残留
                    if s(resourceId=
                         "com.android.packageinstaller:id/install_confirm_panel"
                         ).exists:
                        # 通过偏移点击<安装>
                        s(resourceId=
                          "com.android.packageinstaller:id/bottom_button_layout"
                          ).click(offset=(0.5, 0.2))
                    elif s(text=u"知道了").exists:
                        raise Exception('已经安装高版本，请卸载重装')
                btn_done.click()

        else:
            cls.watch_device(['允许', '继续安装', '允许安装', '始终允许', '安装', '重新安装'])
            r = cls.d.shell(['pm', 'install', '-r', dst], stream=True)
            id = r.text.strip()
            print(time.strftime('%H:%M:%S'), id)
            cls.unwatch_device()
        cls.d.shell(['rm', dst])

    @classmethod
    def unlock_device(cls):
        '''unlock.apk install and launch'''
        pkgs = re.findall('package:([^\s]+)', cls.d.shell(['pm', 'list', 'packages', '-3'])[0])
        if 'io.appium.unlock' in pkgs:
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')
        else:
            #  appium unlock.apk 下载安装
            print('installing io.appium.unlock')
            cls.d.app_install('https://raw.githubusercontent.com/pengchenglin/ATX-GT/master/apk/unlock.apk')
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')

    @classmethod
    def identify(cls):
        cls.d.open_identify()

    @classmethod
    def watch_device(cls, watch_list):
        '''
        如果存在元素则自动点击
        :param watch_list: exp: watch_list=['允许','yes','跳过']
        '''
        cls.d.watchers.watched = False
        for i in watch_list:
            cls.d.watcher(i).when(text=i).click(text=i)
            # cls.d.watcher("允许").when(text="允许").click(text="允许")
        print('Starting watcher,parameter is %s' % watch_list)
        cls.d.watchers.watched = True

    @classmethod
    def unwatch_device(cls):
        '''关闭watcher '''
        print('Stop all watcher')
        cls.d.watchers.watched = False


if __name__ == '__main__':
    device = Maxim()
    device.set_driver('192.168.3.26')
    device.d.healthcheck()
    # # device.clear_env()
    command = device.command(package='com.quvideo.xiaoying', runtime=2, mode='uiautomatormix', throttle=100,
                             options=' -v -v ', whitelist=False, off_line=True)
    print(command)
    device.run_monkey(command)
    # print(device.d.shell(command))

    string = "CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.quvideo.xiaoying --uiautomatormix --running-minutes 2 -v -v"
    print(string)
    # device.d.shell(string)
