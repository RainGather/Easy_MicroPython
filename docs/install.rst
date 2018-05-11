安装与快速开始
===================

首先你需要一块NodeMCU板，推荐基于ESP32的，功能更强大，基于ESP8266的也可以使用大部分的功能。

之后将你的NodeMCU板刷入MicroPython框架，具体方法可以查看 `MicroPython官网 <http://www.micropython.org/>`_

本框架本质上是一些封装好函数的py文件，放置于NodeMCU的根目录即可正常使用。

项目提供了一个自动刷入的程序，如果你对NodeMCU不熟悉，可以跟着以下步骤直接使用：

1. 下载本项目：https://github.com/RainGather/Easy_MicroPython/releases
#. 解压到一个目录中，例如：C:\\nodemcu，请保证整个路径没有空格和中文，同时请务必放在C盘（放在其它盘符可能会导致未知的错误）
#. 安装Python 3，同时请将Python路径加入到环境变量PATH中
#. 将NodeMCU连接上电脑
#. 双击flash.bat运行，第一次运行时，会自动尝试安装缺失的库文件，安装完后需关闭重新打开。
#. 按指示选择端口和设备型号，等待框架刷入完成后关闭窗口。
#. 在该目录下，新建HelloWorld.py，在里面可以写入本手册中的案例代码。例如::

    print('Hello World')
#. 双击upload.bat
#. 按照指示选择端口和需刷入的文件，文件会自动列出在列表中，填写数字序号即可。
#. 显示刷入成功后，按下[CTRL + D]或板子上的[RST]键重启板子运行。
#. 如果一切正常，刷入窗口最后应该会出现Hello World字样。
#. 窗口关闭后，可用用connect.bat重新连接至NodeMCU。
