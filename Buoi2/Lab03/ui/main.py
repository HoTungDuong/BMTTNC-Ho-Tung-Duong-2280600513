import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from rsa import Ui_MainWindow
import rsa

if not os.path.exists('cipher/rsa/keys'):
    os.makedirs('cipher/rsa/keys')

class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        with open('cipher/rsa/keys/publicKey.pem', 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open('cipher/rsa/keys/privateKey.pem', 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))

    def load_keys(self):
        with open('cipher/rsa/keys/publicKey.pem', 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open('cipher/rsa/keys/privateKey.pem', 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('ascii'), key)

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False

    def sign(self, message, key):
        return rsa.sign(message.encode('ascii'), key, 'SHA-1')

    def verify(self, message, signature, key):  # Sửa lỗi cú pháp
        try:
            return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-1'
        except:
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rsa_cipher = RSACipher()
        self.ui.txt_Generate.clicked.connect(self.call_generate_keys)
        self.ui.pushButton_2.clicked.connect(self.call_encrypt)
        self.ui.pushButton_3.clicked.connect(self.call_decrypt)
        self.ui.pushButton_4.clicked.connect(self.call_sign)
        self.ui.pushButton_5.clicked.connect(self.call_verify)

    def call_generate_keys(self):
        try:
            self.rsa_cipher.generate_keys()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Keys generated successfully!")
            msg.exec_()
        except Exception as e:
            print(f"Error: {e}")

    def call_encrypt(self):
        try:
            private_key, public_key = self.rsa_cipher.load_keys()
            message = self.ui.plainTextEdit.toPlainText()
            if message:
                encrypted = self.rsa_cipher.encrypt(message, public_key)
                self.ui.plainTextEdit_3.setText(encrypted.hex())
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully!")
                msg.exec_()
        except Exception as e:
            print(f"Error: {e}")

    def call_decrypt(self):
        try:
            private_key, public_key = self.rsa_cipher.load_keys()
            ciphertext = bytes.fromhex(self.ui.plainTextEdit_3.toPlainText())  # Sửa lỗi cú pháp
            decrypted = self.rsa_cipher.decrypt(ciphertext, private_key)
            if decrypted:
                self.ui.plainTextEdit.setText(decrypted)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully!")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Decryption Failed!")
                msg.exec_()
        except Exception as e:
            print(f"Error: {e}")

    def call_sign(self):
        try:
            private_key, public_key = self.rsa_cipher.load_keys()
            message = self.ui.plainTextEdit_2.toPlainText()
            if message:
                signature = self.rsa_cipher.sign(message, private_key)
                self.ui.plainTextEdit_4.setText(signature.hex())
                msg = QMessageBox()  # Sửa lỗi: khởi tạo biến msg
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully!")
                msg.exec_()
        except Exception as e:
            print(f"Error: {e}")

    def call_verify(self):
        try:
            private_key, public_key = self.rsa_cipher.load_keys()
            message = self.ui.plainTextEdit_2.toPlainText()
            signature = bytes.fromhex(self.ui.plainTextEdit_4.toPlainText())
            if message and signature:
                verified = self.rsa_cipher.verify(message, signature, public_key)
                msg = QMessageBox()
                if verified:
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully!")
                else:
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Verification Failed!")
                msg.exec_()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())