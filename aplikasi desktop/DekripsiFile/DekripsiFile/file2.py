import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contoh Halaman Kedua")
        self.setGeometry(200, 200, 400, 500)

        self.button = QPushButton("Tampilkan Halaman Kedua", self)
        self.button.clicked.connect(self.show_second_page)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def show_second_page(self):
        self.second_page = SecondPage()
        self.setCentralWidget(self.second_page)



class SecondPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contoh Tampilan HTML")
        self.setGeometry(100, 100, 800, 600)

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        self.load_html_content()

    def load_html_content(self):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }

                h1 {
                    color: #333;
                }

                p {
                    margin-bottom: 10px;
                }

                button {
                    padding: 10px 20px;
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Informasi File</h1>
            <p>Nama File: <span id="file_name"></span></p>
            <p>Waktu Dekripsi: <span id="decryption_time"></span></p>
            <p>Ukuran File: <span id="file_size"></span></p>
            <button id="decrypt_button">Download</button>

            <script>
                // Fungsi untuk mengisi informasi file
                function fillFileInfo(name, time, size) {
                    document.getElementById('file_name').textContent = name;
                    document.getElementById('decryption_time').textContent = time;
                    document.getElementById('file_size').textContent = size;
                }

                // Event listener untuk tombol dekripsi
                document.getElementById('decrypt_button').addEventListener('click', function() {
                    // Tambahkan logika dekripsi di sini
                    alert('Proses dekripsi...');
                });

                // Panggil fungsi fillFileInfo dengan data file yang diinginkan
                fillFileInfo('nama_file.txt', '10:30', '1.2 MB');
            </script>
        </body>
        </html>
        """

        base_url = QUrl.fromLocalFile(".")

        self.web_view.setHtml(html_content, base_url)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
