安装与快速开始
===================

首先你需要一块NodeMCU板，推荐是基于ESP32的，功能更强大，基于ESP8266的也可以使用大部分的功能。

之后将你的NodeMCU板刷入MicroPython框架，具体方法可以查看:`MicroPython官网 <http://www.micropython.org/>`_

随后可以用Python 3.X运行flash_lib.py，跟着指示即可将本库刷入到NodeMCU中。

刷入成功后，设备中就会有一个可以使用的ezmpy库，可以用如下代码导入::

    from ezmpy import *

在电脑中新建一个main.py文件，将如下内容写入文件中::

    from ezmpy import *
    print('Hello World')

将该文件放置于项目根目录之下，重新运行flash.py，按照指示把该文件烧入即可。

烧录后，按下[CTRL + D]或板子上的[RST]键重启板子运行。

如果一切正常，应该会出现Hello World字样。
