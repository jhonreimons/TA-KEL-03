import sys, os
from PyQt5.QtWidgets import QProgressBar, QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import QTimer,Qt,QThread, pyqtSignal
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from base64 import b64decode
from getpass import getpass
from PyQt5.QtGui import QMovie
import time
from PyQt5 import QtCore
import threading
from PyQt5.QtCore import QSettings
from cryptography.hazmat.primitives.asymmetric import padding

class FileDecryptionApp(QMainWindow):
    def __init__(self):
        super(FileDecryptionApp, self).__init__()

        # Membuat tampilan utama
        self.setWindowTitle("Aplikasi Dekripsi File")
        self.setGeometry(500, 300, QApplication.desktop().width(), QApplication.desktop().height())

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

        # Membuat tombol untuk memulai proses dekripsi
        self.button_decrypt = QPushButton("Dekripsi")
        self.layout.addWidget(self.button_decrypt)

        # Mengatur layout ke dalam widget utama
        self.tittle = QLabel("Informasi Hasil Enkripsi")
        self.file_label = QLabel("Nama file: ")
        self.size_label = QLabel("Ukuran file: ")
        self.time_label = QLabel("Waktu dekripsi: ")

        self.layout.addWidget(self.tittle)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.time_label)
        self.central_widget.setLayout(self.layout)

        # self.button_decrypt.clicked.connect(self.start_loading)
        # Menghubungkan sinyal dan slot
        self.button_choose_file.clicked.connect(self.choose_file)
        self.button_decrypt.clicked.connect(self.decrypt_file)

        #membuat choose file terhubung ke last directory
        self.settings = QSettings('MyCompany', 'MyApp')
        self.last_directory = self.settings.value('last_directory', '.')

        # self.settings2 = QSettings('MyCompany', 'MyApp')
        # self.last_directory2 = self.settings2.value('last_directory', '.')


    def choose_file(self):
        # Memilih file yang akan didekripsi
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Pilih File untuk Dekripsi", self.last_directory, f'All Files (*.enc)')
        self.file_path = self.file_name
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
            # file_name = file.name[:-4]
            # Mengimpor private key
            private_key = RSA.import_key(private_key, passphrase=passphrase)
            cipher = PKCS1_OAEP.new(private_key)
            # PKCS1_OAEP, PKCS1_v1_5
            # decrypted_data = b''
            # Menyimpan file hasil dekripsi
            decrypted_chunks = []
            # threads = []
            start_time = time.time()
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i+chunk_size]
                decrypted_chunks.append(self.decrypt_chunk(cipher, chunk))

            decrypted_data = b''.join(decrypted_chunks)
            end_time = time.time()
            elapsed_time = start_time - end_time
            # file_ext = self.file_name[-8:]
            # file_ext = os.path.splitext(file_ext)[0]
            fileName = self.file_name
            split_name = fileName.split(".", 1)
            num_characters = len(split_name[1])
            if num_characters == 10:
                fileName = fileName[:-7]
                print(file_name)


            if num_characters == 7:
                fileName = fileName[:-4]
            split_name = fileName.split(".", 1)
            file_ext = split_name[1]
            output_file_name, _ = QFileDialog.getSaveFileName(self, "Simpan File Hasil Dekripsi", self.last_directory, f'All Files (*.{file_ext})')

            with open(output_file_name, 'wb') as output_file:
                output_file.write(decrypted_data)

            file_name = os.path.basename(output_file_name)
            file_size = os.path.getsize(output_file_name)
            units = ['B', 'KB', 'MB', 'GB', 'TB']
            index = 0

            while file_size >= 1024 and index < len(units):
                file_size /= 1024
                index += 1

            if index >= len(units):
                index = len(units) - 1

            file_size_formatted = f'{file_size:.2f} {units[index]}'

            file_size = f"{file_size_formatted}"
            waktu = abs(elapsed_time)
            elapsed_time = f"{waktu:.2f}"
            self.tittle.setText("Informasi Hasil Dekripsi")
            self.file_label.setText("Nama file: " + file_name )
            self.size_label.setText("Ukuran file: " + file_size)
            self.time_label.setText("Waktu dekripsi: " + elapsed_time + "detik")
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
