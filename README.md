# 百度网盘定时下载

## 本地调试

程序可以在 windows 或 mac 电脑上运行，但需要先安装 python3 和 chrome，他们可以在如下网址进行下载：

* https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
* https://www.google.cn/chrome/

上面安装完成后，进入当前目录，执行如下操作：

* 安装依赖： `pip install -r requirements.txt`
* 配置环境变量 (mac电脑不需要)：在 `PATH` 环境变量中添加 `C:\Program Files (x86)\Google\Chrome\Application`
* 配置参数：在 `resources/config.yaml` 中配置要下载的文件路径：
  * dirPath： 文件所在的目录网址
  * fileName： 文件名
  * downloadInterval： 间隔多少分钟下载一次文件
* 启动程序：执行 `python main.py`
* 首次启动程序，需要在打开的浏览器中，登录百度账号，后面就不需要了

## 部署

安装打包工具 `pyinstaller`, 安装命令为 `pip install pyinstaller`。 

用 `pyinstaller main.py -n baidu -F -i logo.ico` 进行打包，然后把 `dist` 压缩后发到对应的机器上进行运行即可。

## 其他

注意：程序运行过程中，可以最小化程序启动的 chrome 浏览器，但不要关闭。