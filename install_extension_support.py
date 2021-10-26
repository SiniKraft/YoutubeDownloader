import winreg
import os
import logo_rc

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QMessageBox, QApplication

key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'nickloryoutubedl')
winreg.SetValue(key, r'shell\open\command', winreg.REG_SZ, '"' + os.path.join(
    os.getcwd(), "extension-launcher.exe") + '" "%1"')
winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
winreg.CloseKey(key)

app = QApplication()

msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setWindowIcon(QIcon(QPixmap(u":/img/icon-256.png")))
msg.setWindowTitle("Youtube Downloader By Nicklor")
msg.setText("Extension support successfully installed !")
msg.show()

app.exec_()
