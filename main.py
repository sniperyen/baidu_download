import datetime
import multiprocessing

import os
import pathlib
import platform
import subprocess
import time
from multiprocessing import Process
import logging
from logging.handlers import RotatingFileHandler
import yaml

from util.browser import get_driver, get_opts
import util.mul_process_package  # 防止打包exe后启动，程序卡死

# 读取配置文件
path = os.path.join(os.curdir, 'resources', 'config.yaml')
with open(path, 'r', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(processName)s][%(filename)s][line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[RotatingFileHandler('run.log', maxBytes=10 * 1024 * 1024, backupCount=5), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
logger.info("----------hello world---------")

# 创建浏览器的用户目录
user_data_dir = os.path.join(os.curdir, 'AutomationProfile')
pathlib.Path(user_data_dir).mkdir(parents=True, exist_ok=True)
remote_debugging_port = 9527


def start_debug_chrome():
    logger.info("启动浏览器")
    if platform.system() == 'Windows':
        chrome_path = 'chrome.exe'
        os.system('taskkill /im chrome.exe')
        start_command = 'start %s --remote-debugging-port=%d --user-data-dir=%s' % (
            chrome_path, remote_debugging_port, user_data_dir)
        logger.info(start_command)
        os.system(start_command)

    elif platform.system() == 'Darwin':
        chrome_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        start_command = "%s --remote-debugging-port=%s --user-data-dir=%s" % (
            chrome_path, remote_debugging_port, user_data_dir)
        logger.info(start_command)
        subprocess.Popen(start_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, )
    else:
        raise Exception("不支持此操作系统：%s" % platform.system())


def start_baidu_download():
    dir_path = cfg.get('downloadLocation').get('dirPath')
    file_name = cfg.get('downloadLocation').get('fileName')
    download_interval = cfg.get('downloadInterval')

    debugger_address = "127.0.0.1:%d" % remote_debugging_port
    opts = get_opts(is_visible=True, debugger_address=debugger_address)
    if platform.system() == 'Windows':
        chromedriver_path = os.path.join(os.curdir, "resources", "chromedriver.exe")
    elif platform.system() == 'Darwin':
        chromedriver_path = os.path.join(os.curdir, "resources", "chromedriver")
    else:
        raise Exception("不支持此操作系统：%s" % platform.system())
    driver = get_driver(opts, executable_path=chromedriver_path)

    def close_popup_box():
        # 弹窗有时候有，有时候无
        logger.info('检查是否有弹窗')
        close_buttons = driver.find_elements_by_class_name("close-mask")
        if close_buttons:
            logger.info('关闭弹出框')
            time.sleep(1)
            close_buttons[0].click()

        close_buttons = driver.find_elements_by_id("dialog1")
        if close_buttons:
            logger.info('关闭弹出框')
            time.sleep(1)
            close_buttons[0].click()

    def run():
        t = 0
        while True:
            driver.get(dir_path)
            driver.maximize_window()
            if driver.title != '百度网盘-全部文件':
                t += 1
                logger.info("重试次数：%d -- 请先在浏览器中登陆网盘，然后稍等片刻(一分钟)～" % t)
                time.sleep(60)
                continue
            break

        logger.info('进入了网盘主页面')
        close_popup_box()

        # 先判断目录下是否有文件
        dds = driver.find_elements_by_xpath('//dd[contains(@class, "g-clearfix")]')
        if not dds:
            raise Exception("此目录下没有任何文件")

        # 遍历目录下所有文件，勾选需要下载的文件
        for dd in dds:
            text = dd.find_element_by_xpath('div[@class="file-name"]/div[@class="text"]').text
            if file_name in text:
                logger.info("找到需要下载的文件，勾选")
                close_popup_box()
                dd.find_element_by_xpath('span').click()
                break

        # 勾选完后，点击下载按钮
        bts = driver.find_elements_by_xpath('//a[@title="下载"][@data-button-index="5"]')
        if not bts:
            raise Exception("找不到下载按钮")

        logger.info('准备点击下载按钮')
        bts[0].click()
        logger.info("开始下载，请不要关闭浏览器")

    try:
        while True:
            run()
            next_time = datetime.datetime.now() + datetime.timedelta(minutes=download_interval)
            logger.info("下次下载时间为 %s" % next_time.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(download_interval * 60)
    finally:
        driver.quit()


def main():
    process_list = []

    p1 = Process(target=start_debug_chrome, args=(), name='chrome')
    p1.start()
    process_list.append(p1)

    p2 = Process(target=start_baidu_download, args=(), name='download')
    p2.start()
    process_list.append(p2)

    for p in process_list:
        p.join()

    logger.info('结束程序')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
    # start_debug_chrome()
