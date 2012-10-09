#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

app = QApplication(sys.argv)

web = QWebView()

web.settings().setAttribute(
    QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)

web.load(QUrl("http://twitter.github.com/bootstrap/"))
web.show()

inspect = QWebInspector()
inspect.setPage(web.page())
inspect.show()

sys.exit(app.exec_())
