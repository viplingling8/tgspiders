# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QEventLoop, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication


class Render(QWebEngineView):
    """Render HTML with PyQt5 WebEngine."""

    def __init__(self, html):
        self.html = None
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(html))
        while self.html is None:
            self.app.processEvents(
                QEventLoop.ExcludeUserInputEvents |
                QEventLoop.ExcludeSocketNotifiers |
                QEventLoop.WaitForMoreEvents)
        self.app.quit()

    def _callable(self, data):
        self.html = data

    def _loadFinished(self, result):
        self.page().toHtml(self._callable)


if __name__ == '__main__':
    r = Render('https://www.cctd.com.cn/list-167-1.html')
    html = r.html
    print(html)
