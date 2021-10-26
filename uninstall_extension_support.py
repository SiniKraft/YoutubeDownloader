import winreg
import os
import logo_rc

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QMessageBox, QApplication

key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'nickloryoutubedl')
winreg.DeleteKey(key, r"shell\open\command")
winreg.DeleteKey(key, r"shell\open")
winreg.DeleteKey(key, r"shell")
winreg.DeleteKey(key, r"")
winreg.CloseKey(key)

app = QApplication()

msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setWindowIcon(QIcon(QPixmap(u":/img/icon-256.png")))
msg.setWindowTitle("Youtube Downloader By Nicklor")
msg.setText("Extension support successfully uninstalled !")
msg.show()

app.exec_()
