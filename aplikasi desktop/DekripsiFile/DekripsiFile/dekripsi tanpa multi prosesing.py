import sys
from PyQt5.QtWidgets import QProgressBar, QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer,Qt,QThread, pyqtSignal
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
from getpass import getpass
from PyQt5.QtGui import QMovie
import time
from PyQt5 import QtCore
import threading
from PyQt5.QtCore import QSettings

elapsed_time = 0
class FileDecryptionApp(QMainWindow):
    def __init__(self):
        super(FileDecryptionApp, self).__init__()

        # Membuat tampilan utama
        self.setWindowTitle("Aplikasi Dekripsi File")
        self.setGeometry(500, 200, QApplication.desktop().width(), QApplication.desktop().height())

        # Membuat widget utama
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Membuat layout vertikal
        self.layout = QVBoxLayout()

        # Membuat label untuk menampilkan pesan
        self.label = QLabel()
        self.layout.addWidget(self.label)

        # Membuat tombol untuk memilih file
        self.button_choose_file = QPushButton("Pilih File untuk Dekripsi")
        self.layout.addWidget(self.button_choose_file)

        # untuk menampilkan nama file
        self.labelFile = QLabel(self)
        self.layout.addWidget(self.labelFile)

        # Membuat teks box untuk memasukkan private key
        self.private_key_text = QTextEdit()
        self.private_key_text.setPlaceholderText("Masukkan Private Key")
        self.layout.addWidget(self.private_key_text)

        # Membuat line edit untuk memasukkan passphrase
        self.passphrase_edit = QLineEdit()
        self.passphrase_edit.setPlaceholderText("Masukkan Passphrase")
        self.passphrase_edit.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passphrase_edit)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Membuat tombol untuk memulai proses dekripsi
        self.button_decrypt = QPushButton("Dekripsi")
        self.layout.addWidget(self.button_decrypt)

        # Mengatur layout ke dalam widget utama
        self.central_widget.setLayout(self.layout)

        # self.button_decrypt.clicked.connect(self.start_loading)

        # Menyembunyikan progress bar saat aplikasi dimulai
        self.progress_bar.hide()

        # Menghubungkan sinyal dan slot
        self.button_choose_file.clicked.connect(self.choose_file)
        self.button_decrypt.clicked.connect(self.decrypt_file)

        #membuat choose file terhubung ke last directory
        self.settings = QSettings('MyCompany', 'MyApp')
        self.last_directory = self.settings.value('last_directory', '.')


    def choose_file(self):
        # Memilih file yang akan didekripsi
        file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File untuk Dekripsi", self.last_directory, 'All Files (*)')
        self.file_path = file_name
        self.labelFile.setText("File yang akan didekripsi: {}".format(self.file_path))

    def decrypt_chunk(self, cipher, chunk):
        return cipher.decrypt(chunk)

    def decrypt_file(self):
        chunk_size = 256
        # Memeriksa apakah file telah dipilih
        if not hasattr(self, 'file_path'):
            QMessageBox.warning(self, "Peringatan", "Pilih file terlebih dahulu!")
            return

        # Memeriksa apakah private key telah dimasukkan
        private_key = self.private_key_text.toPlainText()
        if not private_key:
            QMessageBox.warning(self, "Peringatan", "Masukkan private key terlebih dahulu!")
            return

        # Memeriksa apakah passphrase telah dimasukkan
        passphrase = self.passphrase_edit.text()
        if not passphrase:
            QMessageBox.warning(self, "Peringatan", "Masukkan passphrase terlebih dahulu!")
            return

        try:
            with open(self.file_path, 'rb') as file:
                content = file.read()
            file_name = file.name[:-4]
            # Mengimpor private key
            private_key = RSA.import_key(private_key, passphrase=passphrase)
            cipher_rsa = PKCS1_OAEP.new(private_key)
            decrypted_data = b''
            # Menyimpan file hasil dekripsi
            start_time = time.time()
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i + chunk_size]
                padded_chunk = cipher_rsa.decrypt(chunk)  # Menggunakan fungsi decrypt() untuk mendekripsi data
                decrypted_data += padded_chunk
            end_time = time.time()
            global elapsed_time
            elapsed_time = end_time - start_time

            output_file_name, _ = QFileDialog.getSaveFileName(self, "Simpan File Hasil Dekripsi")
            with open(output_file_name, 'wb') as output_file:
                output_file.write(decrypted_data)

            self.label.setText("File berhasil didekripsi dan disimpan sebagai: {}".format(output_file_name))
            QMessageBox.information(self, "Informasi", "Proses dekripsi selesai!")
        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", "Terjadi kesalahan: {}".format(str(e)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileDecryptionApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
