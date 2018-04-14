安装与快速开始
===================

首先你需要一块NodeMCU板，推荐基于ESP32的，功能更强大，基于ESP8266的也可以使用大部分的功能。

之后将你的NodeMCU板刷入MicroPython框架，具体方法可以查看:`MicroPython官网 <http://www.micropython.org/>`_

本框架本质上是一些封装好函数的py文件，放置于NodeMCU的根目录即可正常使用。

项目提供了一个自动刷入的程序，如果你对NodeMCU不熟悉，可以跟着以下步骤直接使用：

1. 下载本项目：https://github.com/RainGather/Easy_MicroPython/archive/release.zip
2. 解压到一个目录中，例如：C:\nodemcu，请保证整个路径没有空格和中文，同时请务必放在C盘（放在其它盘符可能会导致未知的错误）
3. 在该目录下，新建HelloWorld.py，在里面可以写入本手册中的案例代码。例如::
    print('Hello World')
4. 安装Python 3，同时请将Python路径加入到环境变量PATH中
5. 双击flash.bat运行
6. 选择端口(Windows下一般是类似COM + 数字的组合，例如COM3，需要在设备管理器中查看。如果你不会查看，可以直接按回车，刷入软件会尝试自动寻找。但是由于不名原因，第一次寻找到的可能性很低，需要关闭后重新运行一次才能找到。)
7. 选择需要刷入的文件。程序会列出根目录下的文件，可以将你在第3步中新建的文件刷入。刷入文件时，会自动重新刷入一遍Easy MicroPython框架。
8. 显示刷入成功后，按下[CTRL + D]或板子上的[RST]键重启板子运行。
9. 如果一切正常，刷入窗口最后应该会出现Hello World字样。
