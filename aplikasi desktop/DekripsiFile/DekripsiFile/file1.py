from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

app = QApplication([])

# Membuat WebView
web_view = QWebEngineView()

# Mengeset konten HTML pada WebView
html_path = "D:/AplikasiDesktop/DekripsiFile/DekripsiFile/index.html"
with open(html_path, 'r') as file:
    html_content = file.read()

web_view.setHtml(html_content, QUrl.fromLocalFile(html_path))

# Menampilkan WebView window
web_view.show()

# Data yang akan dikirim ke halaman HTML
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Mengkonversi data menjadi JSON
json_data = json.dumps(data)

# Mengirim data ke halaman HTML menggunakan JavaScript
web_view.page().runJavaScript(f"displayData({json_data})")
