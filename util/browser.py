import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_opts(is_visible=False, host_port='', user_agent='', debugger_address='', binary_location='') -> Options:
    # 启动参数列表:  https://peter.sh/experiments/chromium-command-line-switches/
    # selenium 启动 Chrome配置参数问题 https://zhuanlan.zhihu.com/p/60852696

    opts = Options()
    if not is_visible:
        opts.add_argument("log-level=3")
        # 浏览器不提供可视化页面. linux 下如果系统不支持可视化不加这条会启动失败
        opts.add_argument("--headless")
        # 以最高权限运行
        opts.add_argument('--no-sandbox')
        # 代理
        # opts.add_argument("--proxy-server=socks5://103.254.151.179:4565")

    # 添加代理服务
    if host_port:
        # 代理软件使用方法: browsermob-proxy
        opts.add_argument('--proxy-server=socks5://%s' % host_port)

    # 添加 user-agent
    if not user_agent:
        # https://www.jianshu.com/p/9453579154e3
        # 普通格式: User-Agent: Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        opts.add_argument('user-agent="%s"' % user_agent)

    # 手动指定浏览器位置
    if binary_location:
        opts.binary_location = binary_location

    # 调试地址
    if debugger_address:
        opts.add_experimental_option("debuggerAddress", debugger_address)

    # 设置开发者模式启动，该模式下 window.navigator.webdriver 属性为正常值，否则会被网站监测到
    # opts.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 最大化运行（全屏窗口）
    opts.add_argument("--start-maximized")
    # # 指定浏览器分辨率
    # opts.add_argument('window-size=1920x3000')
    # 解决跨域问题
    opts.add_argument("--disable-web-security")
    # # 禁用浏览器正在被自动化程序控制的提示
    # opts.add_argument("--disable-infobars")
    # 谷歌文档提到需要加上这个属性来规避bug
    opts.add_argument("--disable-gpu")
    # 解决混合内容问题，不看到不安全内容的提示
    opts.add_argument("--allow-running-insecure-content")
    # # 隐藏滚动条, 应对一些特殊页面
    # opts.add_argument('--hide-scrollbars')
    # # 不加载图片, 提升速度
    # opts.add_argument('blink-settings=imagesEnabled=false')

    # # 添加扩展应用
    # opts.add_extension()
    # opts.add_encoded_extension()
    #
    # # 设置调试器地址
    # opts.debugger_address()
    #
    # # 添加crx插件
    # opts.add_extension('d:\crx\AdBlock_v2.17.crx')
    #
    # # 禁用JavaScript
    # opts.add_argument("--disable-javascript")
    #

    #
    # # 禁用浏览器弹窗
    # prefs = {
    #     'profile.default_content_setting_values': {
    #         'notifications': 2
    #     }
    # }
    # opts.add_experimental_option('prefs', prefs)

    return opts


def get_driver(opts, executable_path='', implicitly_wait=5, page_load_timeout=30):
    capabilities = webdriver.DesiredCapabilities.CHROME
    if not executable_path:
        _driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts,
                                   desired_capabilities=capabilities)
    else:
        _driver = webdriver.Chrome(executable_path=executable_path, options=opts,
                                   desired_capabilities=capabilities)

    _driver.implicitly_wait(implicitly_wait)
    _driver.set_page_load_timeout(page_load_timeout)
    return _driver


if __name__ == '__main__':
    host_port = ''
    opts = get_opts(is_visible=True, is_mobile=False, host_port=host_port)
    driver = get_driver(opts)
    try:
        driver.get('http://www.cip.cc')
        time.sleep(20000)
    finally:
        driver.quit()
