import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Communication(QObject):
    valueChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._value = ""

    @pyqtSlot(str)
    def setValue(self, value):
        if self._value != value:
            self._value = value
            self.valueChanged.emit(self._value)

    @pyqtSlot(result=str)
    def getValue(self):
        return self._value


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Membuat objek QApplication
    web_view = QWebEngineView()

    # Membuat objek QWebChannel
    channel = QWebChannel()
    communication = Communication()
    channel.registerObject('communication', communication)
    web_view.page().setWebChannel(channel)

    # Meload file HTML
    web_view.load(QUrl.fromLocalFile('D:\AplikasiDesktop\DekripsiFile\DekripsiFile\index.html'))

    # Menghubungkan sinyal valueChanged dengan fungsi untuk memperbarui nilai dalam HTML
    communication.valueChanged.connect(lambda value: web_view.page().runJavaScript("updateValue('{}')".format(value)))

    # Menampilkan jendela utama
    window = QMainWindow()
    window.setCentralWidget(web_view)
    window.show()

    sys.exit(app.exec_())
