#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()
web.load(QUrl("http://acid3.acidtests.org/"))
web.show()

sys.exit(app.exec_())
