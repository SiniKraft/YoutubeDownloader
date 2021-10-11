import sys
import os
import threading
import time
import tkinter.messagebox
import urllib.request
import pathlib
import logging
import io
import webbrowser

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QObject, Slot, Signal

from ui_main_window import Ui_MainWindow
from ui_path_dialog import Ui_PathDialog

from pytube import YouTube

log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.DEBUG, format="%(message)s")

pref_path = os.path.join(str(pathlib.Path().home()), ".NicklorYoutubeDownloader/")
os.makedirs(pref_path, exist_ok=True)
if sys.platform == "win32":
    import ctypes

    ctypes.windll.kernel32.SetFileAttributesW(pref_path, 0x02)
if not os.path.isfile(pref_path + "pathPreference"):
    path_preference = os.path.join(str(pathlib.Path().home()), "Downloads")
    with open(os.path.join(pref_path, "pathPreference"), "w+") as file:
        file.write(path_preference)
        file.close()
else:
    with open(os.path.join(pref_path, "pathPreference"), "r") as file:
        path_preference = file.read()
        file.close()


@Slot(str)
def exec_sth(value):
    exec(value)


@Slot(int)
def update_bar(value):
    main_window.progressBar.setValue(value)


@Slot(str)
def _show_msg(value):
    msgbox = QMessageBox(parent=main_window)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setWindowTitle("Youtube Downloader by Nicklor")
    msgbox.setText(value)
    msgbox.exec_()



class Communicate(QObject):
    # signal_str = Signal(str)
    signal_int = Signal(int)
    signal_str = Signal(str)
    signal_str_2 = Signal(str)

    def use_signal_str(self, value):
        self.signal_str.emit(value)

    def use_signal_int(self, value):
        self.signal_int.emit(value)

    def show_msg(self, value):
        self.signal_str_2.emit(value)


class PathDialog(QDialog, Ui_PathDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Downloads location")
        self.lineEdit.setText(parent.path_preference)
        self.buttonBox.accepted.connect(lambda: self.save_pref(parent))
        self.pushButton.clicked.connect(self.open_folder)

    def save_pref(self, parent):
        parent.path_preference = self.lineEdit.text()
        with open(os.path.join(pref_path, "pathPreference"), "w+") as file__:
            file__.write(parent.path_preference)
            file__.close()

    def open_folder(self):
        selected_path = QFileDialog.getExistingDirectory(self, "Choose a Folder", path_preference)
        if not selected_path == "":
            self.lineEdit.setText(selected_path)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.path_preference = path_preference
        self.clearButton.hide()
        self.setWindowIcon(QIcon(QPixmap(u":/img/youtube_play1600.png")))
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.setup_connections()
        self.setWindowTitle("Youtube Downloader by Nicklor")
        self.video_selection = None
        self.audio_selection = None
        self.ys = None
        self.vid_select_itag = None
        self.aud_select_itag = None
        self.done_video = False
        self.lineEdit.setFocus()
        self.clearButton.hide()
        self.dl_mode = 0
        self.thread_download_aud = None
        self.thread_download_vid = None
        self.thread_listen_bar = None
        self.signals = Communicate()
        self.signals.signal_int.connect(update_bar)
        self.signals.signal_str.connect(exec_sth)
        self.signals.signal_str_2.connect(_show_msg)

    def setup_connections(self):
        self.checkBox.toggled.connect(lambda: self.on_checkbox_change(1))
        self.checkBox_2.toggled.connect(lambda: self.on_checkbox_change(2))
        self.SubmitButton.clicked.connect(lambda: self.on_submit_btn(False))
        self.lineEdit.returnPressed.connect(lambda: self.on_submit_btn(False))
        self.listWidget.itemSelectionChanged.connect(lambda: self.selection_changed(1))
        self.listWidget_2.itemSelectionChanged.connect(lambda: self.selection_changed(2))
        self.delButton.clicked.connect(self.delbtnevent)
        self.clearButton.clicked.connect(self.clearButtonEvent)
        self.chooseresbtn.clicked.connect(self.radioButtonManager)
        self.chooseresbtn_2.clicked.connect(self.radioButtonManager)
        self.bestresbtn.clicked.connect(self.radioButtonManager)
        self.bestresbtn_2.clicked.connect(self.radioButtonManager)
        self.actionChange_Downloads_Location.triggered.connect(lambda: self.qactions(1))
        self.commandLinkButton.clicked.connect(self.download_handler)
        self.actionAbout.triggered.connect(lambda: webbrowser.open("https://github.com/SiniKraft/YoutubeDownloader"
                                                                   "#youtubedownloader"))
        self.actionExit.triggered.connect(self.close)

    def on_checkbox_change(self, cknm):
        if cknm == 1:
            if self.checkBox.checkState():
                # when False -> True
                self.chooseresbtn.setEnabled(True)
                self.bestresbtn.setEnabled(True)
                if self.chooseresbtn.isChecked():
                    self.listWidget.setEnabled(True)
            else:
                # when True -> False
                self.bestresbtn.setEnabled(False)
                self.chooseresbtn.setEnabled(False)
                self.listWidget.setEnabled(False)
        elif cknm == 2:
            if self.checkBox_2.checkState():
                self.bestresbtn_2.setEnabled(True)
                self.chooseresbtn_2.setEnabled(True)
                if self.chooseresbtn_2.isChecked():
                    self.listWidget_2.setEnabled(True)
            else:
                self.bestresbtn_2.setEnabled(False)
                self.chooseresbtn_2.setEnabled(False)
                self.listWidget_2.setEnabled(False)
        self.download_btn_manager()

    def download(self):
        try:
            yt = YouTube(self.lineEdit.text())
            self.title_label.setText("Title : " + yt.title)
            self.author_label.setText("Author : " + yt.author)
            self.date_label.setText("Creation date : " + str(yt.publish_date.date()))
            self.views_label.setText("Views : " + str('{:,}'.format(yt.views).replace(',', ' ')))
            self.rating_label.setText("Rating : " + str(round(yt.rating, 2)) + u"/5 \u2605")
            thumbnail = QPixmap()
            thumbnail.loadFromData(urllib.request.urlopen(yt.thumbnail_url).read())
            self.thumbnail_label.setPixmap(thumbnail)
            self.ys = yt.streams
            tmplist = []
            for x in self.ys.filter(type='video').order_by("resolution").desc():
                tmplist.append(x.resolution + " " + str(x.fps) + "fps " + x.subtype + " (itag: " + str(x.itag) + ")")
            self.listWidget.clear()
            self.listWidget.addItems(tmplist)
            tmplist_audio = []
            for x in self.ys.filter(type="audio").order_by('abr').desc():
                tmplist_audio.append(x.abr + " " + x.subtype + " (itag: " + str(x.itag) + ")")
            self.listWidget_2.clear()
            self.listWidget_2.addItems(tmplist_audio)
            self.on_submit_btn(True)
        except Exception as e:
            import tkinter.messagebox
            import tkinter
            win = tkinter.Tk()
            win.withdraw()
            tkinter.messagebox.showerror("Error", str(e))
            win.destroy()
            self.on_submit_btn(True, True)

    def on_submit_btn(self, is_end, error=False):
        if not is_end:
            self.delButton.setDisabled(True)
            self.SubmitButton.setDisabled(True)
            self.lineEdit.setDisabled(True)
            self.progressBar.setMaximum(0)
            self.progressBar.setMinimum(0)
            if self.done_video:
                self.clean()
            thread = threading.Thread(target=self.download)
            thread.start()
        else:
            self.progressBar.setMaximum(100)
            self.SubmitButton.setDisabled(False)
            self.lineEdit.setDisabled(False)
            self.delButton.setDisabled(False)
            if not error:
                self.done_video = True
                self.clearButton.show()
                self.download_btn_manager()
            else:
                self.lineEdit.setFocus()

    def selection_changed(self, list_index):
        if list_index == 1:
            if len(self.listWidget.selectedItems()) == 0:
                self.video_selection = None
            else:
                self.video_selection = self.listWidget.selectedItems()[0].text()
            if self.video_selection is not None:
                self.vid_select_itag = int(self.video_selection.split("(itag: ")[-1][:-1])
            else:
                self.vid_select_itag = None
        elif list_index == 2:
            if len(self.listWidget_2.selectedItems()) == 0:
                self.audio_selection = None
            else:
                self.audio_selection = self.listWidget_2.selectedItems()[0].text()
            if self.audio_selection is not None:
                self.aud_select_itag = int(self.audio_selection.split("(itag: ")[-1][:-1])
            else:
                self.aud_select_itag = None
        self.download_btn_manager()

    def download_btn_manager(self):
        if ((self.checkBox.checkState() and ((self.chooseresbtn.isChecked() and self.vid_select_itag is not None) or
                                             self.bestresbtn.isChecked())) or (self.checkBox_2.checkState()
                                                                               and ((self.chooseresbtn_2.isChecked()
                                                                                     and self.aud_select_itag
                                                                                     is not None) or
                                                                                    self.bestresbtn_2.isChecked()))) \
                and self.done_video:
            self.commandLinkButton.setEnabled(True)
        else:
            self.commandLinkButton.setEnabled(False)

    def delbtnevent(self):
        self.lineEdit.clear()
        self.lineEdit.setFocus()

    def clearButtonEvent(self):
        self.clean()
        self.lineEdit.clear()
        self.clearButton.hide()
        self.lineEdit.setFocus()

    def clean(self):
        self.done_video = False
        self.download_btn_manager()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.author_label.clear()
        self.title_label.clear()
        self.views_label.clear()
        self.rating_label.clear()
        self.date_label.clear()
        self.thumbnail_label.clear()
        self.clearButton.hide()

    def radioButtonManager(self):
        if self.bestresbtn.isChecked():
            self.listWidget.setDisabled(True)
        else:
            self.listWidget.setEnabled(True)
        if self.bestresbtn_2.isChecked():
            self.listWidget_2.setDisabled(True)
        else:
            self.listWidget_2.setEnabled(True)
        self.download_btn_manager()

    def download_handler(self):
        self.clearButton.setDisabled(True)
        self.commandLinkButton.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.SubmitButton.setDisabled(True)
        self.delButton.setDisabled(True)
        self.widget.setDisabled(True)
        self.widget_2.setDisabled(True)
        self.checkBox.setDisabled(True)
        self.checkBox_2.setDisabled(True)
        self.progressBar.setMaximum(1000)
        if self.checkBox.isChecked() and self.checkBox_2.isChecked():
            self.dl_mode = 2  # 1: video only 2 : video + audio 3 : audio only
        elif self.checkBox.isChecked():
            self.dl_mode = 1  # video only
        elif self.checkBox_2.isChecked():
            self.dl_mode = 3  # audio only
        if self.dl_mode == 1 or self.dl_mode == 2:
            if self.dl_mode == 2:
                prefix = "video_"
            else:
                prefix = ""
            if self.bestresbtn.isChecked():
                self.thread_download_vid = threading.Thread(target=self.dl_thread, args=(
                    self.ys.filter(type='video').order_by("resolution").desc().first(), prefix,))
                self.thread_download_vid.start()
                self.thread_listen_bar = threading.Thread(target=self.bar_update_thread, args=(
                    self.ys.filter(type='video').order_by("resolution").desc().first().filesize,))
                self.thread_listen_bar.start()
            else:
                self.thread_download_vid = threading.Thread(target=self.dl_thread, args=(
                    self.ys.get_by_itag(self.vid_select_itag), prefix,))
                self.thread_download_vid.start()
                self.thread_listen_bar = threading.Thread(target=self.bar_update_thread, args=(self.ys.get_by_itag(
                    self.vid_select_itag).filesize,))
                self.thread_listen_bar.start()
        elif self.dl_mode == 3:
            if self.bestresbtn_2.isChecked():
                self.thread_download_aud = threading.Thread(target=self.dl_thread, args=(
                    self.ys.filter(type='audio').order_by("abr").desc().first(), "",))
                self.thread_download_aud.start()
                self.thread_listen_bar = threading.Thread(target=self.bar_update_thread, args=(
                    self.ys.filter(type='audio').order_by("abr").desc().first().filesize, "audio",))
                self.thread_listen_bar.start()
            else:
                self.thread_download_aud = threading.Thread(target=self.dl_thread, args=(
                    self.ys.get_by_itag(self.aud_select_itag), "",))
                self.thread_download_aud.start()
                self.thread_listen_bar = threading.Thread(target=self.bar_update_thread, args=(self.ys.get_by_itag(
                    self.aud_select_itag).filesize, "audio",))
                self.thread_listen_bar.start()

    def dl_thread(self, ys, prefix):
        ys.download(output_path=self.path_preference, filename_prefix=prefix)

    def bar_update_thread(self, filesize, _type='video'):
        def check_if_alive():
            if _type == "video":
                if self.thread_download_vid.is_alive():
                    return True
                return False
            elif _type == "audio":
                if self.thread_download_aud.is_alive():
                    return True
                return False

        while check_if_alive():
            time.sleep(0.1)
            try:
                to_update = int((1 - (int(log_stream.getvalue().split("\n")[-2]
                                          .split("download remaining: ")[-1])) / filesize) * 1000)
                if not (to_update < 0 or to_update > 1000):
                    self.signals.use_signal_int(to_update)
            except Exception as e:
                print(e)
        print("Finished !")
        self.signals.use_signal_int(999)
        if self.dl_mode == 1:
            self.on_dl_finish()

    def qactions(self, num):
        if num == 1:
            path_dialog = PathDialog(self)
            path_dialog.exec_()

    def on_dl_finish(self):
        self.signals.use_signal_int(0)
        self.signals.use_signal_str("main_window.clearButton.setDisabled(False)")
        self.signals.use_signal_str("main_window.commandLinkButton.setDisabled(False)")
        self.signals.use_signal_str("main_window.lineEdit.setDisabled(False)")
        self.signals.use_signal_str("main_window.SubmitButton.setDisabled(False)")
        self.signals.use_signal_str("main_window.delButton.setDisabled(False)")
        self.signals.use_signal_str("main_window.widget.setDisabled(False)")
        self.signals.use_signal_str("main_window.widget_2.setDisabled(False)")
        self.signals.use_signal_str("main_window.checkBox.setDisabled(False)")
        self.signals.use_signal_str("main_window.checkBox_2.setDisabled(False)")
        self.signals.show_msg("The video has been downloaded !\nMessage: %s" % log_stream.getvalue().split("\n")[-2])


app = QApplication(sys.argv)

app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

main_window = MainWindow()

main_window.show()

exit_code = app.exec_()

sys.exit(exit_code)
