import subprocess
import sys
import os
import threading
import time
import urllib.request
import pathlib
import logging
import io
import webbrowser

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QRadioButton
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QObject, Slot, Signal, QRect, QSize

from themes import set_style

from ui_main_window import Ui_MainWindow
from ui_path_dialog import Ui_PathDialog
from ui_convert_dialog import Ui_ConvertDialog
from ui_merging_dialog import Ui_MergingDialog

from pytube import YouTube


class KThread(threading.Thread):
    """A subclass of KThread, with a kill()
    method."""

    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


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

if not os.path.isfile(pref_path + "convSettings"):
    conv_settings = "# Nicklor Youtube Downloader Conversions Settings\n# Parameters : Is convert checkbox checked ?, " \
                    "Last chose conversion format, and existing file check mode.\n# (0: Ask, 1: replace, 2:skip)\n" \
                    "False,MP4,0"
    with open(os.path.join(pref_path, "convSettings"), "w+") as file:
        file.write(conv_settings)
        file.close()
    conv_settings_l = conv_settings.split("\n")[-1].split(",")
    conv_settings_l[0] = conv_settings_l[0] == "True"
    conv_settings_l[2] = int(conv_settings_l[2])
else:
    with open(os.path.join(pref_path, "convSettings"), "r") as file:
        conv_settings = file.read()
        file.close()
    conv_settings_l = conv_settings.split("\n")[-1].split(",")
    conv_settings_l[0] = conv_settings_l[0] == "True"
    conv_settings_l[2] = int(conv_settings_l[2])


def save_conv_settings(_conv_settings_l: list):
    conv_settings = "# Nicklor Youtube Downloader Conversions Settings\n# Parameters : Is convert checkbox checked ?, " \
                    "Last chose conversion format, and existing file check mode.\n# (0: Ask, 1: replace, 2:skip)\n" \
                    + str(_conv_settings_l[0]) + "," + str(_conv_settings_l[1]) + "," + str(_conv_settings_l[2])
    with open(os.path.join(pref_path, "convSettings"), "w+") as ___file:
        ___file.write(conv_settings)
        ___file.close()


if not os.path.isfile(pref_path + "selectedTheme"):
    selected_theme = "System"
    with open(os.path.join(pref_path, "selectedTheme"), "w+") as file:
        file.write(selected_theme)
        file.close()
else:
    with open(os.path.join(pref_path, "selectedTheme"), "r") as file:
        selected_theme = file.read()
        file.close()


def save_theme(theme: str):
    with open(os.path.join(pref_path, "selectedTheme"), "w+") as file:
        file.write(theme)
        file.close()


@Slot(str)
def exec_sth(value: str):
    exec(value)


@Slot(int)
def update_bar(value: int):
    main_window.progressBar.setValue(value)


@Slot(str)
def _show_msg(value: str, _type="info"):
    if _type == "info":
        msgbox = QMessageBox(parent=main_window)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle("Youtube Downloader by Nicklor")
        msgbox.setText(value)
        msgbox.exec_()
    elif _type == "error":
        logging.log(logging.ERROR, str(value))
        msgbox = QMessageBox(parent=main_window)
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Youtube Downloader by Nicklor")
        msgbox.setText("Error : " + value)
        msgbox.exec_()


class Communicate(QObject):
    # signal_str = Signal(str)
    signal_int = Signal(int)
    signal_str = Signal(str)
    signal_str_2 = Signal(str, str)

    def use_signal_str(self, value: str):
        self.signal_str.emit(value)

    def use_signal_int(self, value: int):
        self.signal_int.emit(value)

    def show_msg(self, value: str, type="info"):
        self.signal_str_2.emit(value, type)


class MergingDialog(QDialog, Ui_MergingDialog):
    def __init__(self, parent: "MainWindow", file_1, file_2, output):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Merging files ...")
        parent.merging_state = 1  # merging ...
        self.files = (file_1, file_2)
        self.thread_convert = KThread(target=lambda: parent.convert_handler(file_1, file_2, output))
        self.thread_convert.start()
        self.thread_update = KThread(target=lambda: self.update_thread(parent))
        self.thread_update.start()

    def closeEvent(self, event):
        if main_window.merging_state == 1:
            event.ignore()
        else:
            event.accept()

    def update_thread(self, parent):
        while parent.merging_state == 1:
            parent.signals.use_signal_str('main_window.merge_dialog.plainTextEdit.setPlainText(log_stream.getvalue()'
                                          '.split("Starting merge with arguments: ")[-1])')
            time.sleep(0.01)
        self.close()
        os.remove(os.path.join(parent.path_preference, self.files[0]).replace("\\", "/"))
        os.remove(os.path.join(parent.path_preference, self.files[1]).replace("\\", "/"))


class ConvertDialog(QDialog, Ui_ConvertDialog):
    def __init__(self, parent: "MainWindow"):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Choose export format ...")
        self.buttonBox.accepted.connect(lambda: self.save_conv(parent))

        if "material" in selected_theme:
            self.setMinimumSize(QSize(375, 275))
            self.setMaximumSize(QSize(375, 275))
            self.resize(375, 275)
            self.buttonBox.setGeometry(QRect(20, 220, 341, 52))

        eval("self." + parent.conv_settings[1].lower() + ".setChecked(True)")

    def save_conv(self, parent):
        for radio_btn in self.findChildren(QRadioButton):
            if radio_btn.isChecked():
                parent.conv_settings[1] = radio_btn.objectName().upper()
        save_conv_settings(parent.conv_settings)
        # parent.export_label.setText(parent.conv_settings[1])


class PathDialog(QDialog, Ui_PathDialog):
    def __init__(self, parent: "MainWindow"):
        QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Downloads location")
        self.lineEdit.setText(parent.path_preference)
        self.buttonBox.accepted.connect(lambda: self.save_pref(parent))
        self.pushButton.clicked.connect(self.open_folder)

        if "material" in selected_theme:
            self.setMinimumSize(QSize(362, 151))
            self.setMaximumSize(QSize(362, 151))
            self.resize(362, 151)
            self.verticalLayoutWidget.setGeometry(QRect(20, 9, 321, 121))

    def save_pref(self, parent: QMainWindow):
        parent.path_preference = self.lineEdit.text()
        with open(os.path.join(pref_path, "pathPreference"), "w+") as file__:
            file__.write(parent.path_preference)
            file__.close()
        if not os.path.isdir(parent.path_preference):
            os.makedirs(parent.path_preference)

    def open_folder(self):
        selected_path = QFileDialog.getExistingDirectory(self, "Choose a Folder", path_preference)
        if not selected_path == "":
            self.lineEdit.setText(selected_path)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.merging_state = 0
        self.merge_dialog = None
        self.conv_settings = conv_settings_l
        self.currentDownloadName = ""
        self.cancelDownloadButton.hide()
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
        self.checkBox_3.setChecked(self.conv_settings[0])
        self.is_download_thread_alive = False
        self.theme_actions_mgr()
        self.is_convert_handler_running = False

        if self.conv_settings[2] == 0:
            self.actionAsk_what_to_do.setChecked(True)
        elif self.conv_settings[2] == 1:
            self.actionReplace_file.setChecked(True)
        elif self.conv_settings[2] == 2:
            self.actionSkip_download.setChecked(True)

        if "material" in selected_theme:
            self.lineEdit.setGeometry(QRect(130, 220, 451, 31))

        if not sys.platform == "win32":
            self.actionInstall_extension_compatibility.setDisabled(True)

    def show_dialog(self, file_1, file_2, output):
        self.merge_dialog = MergingDialog(self, file_1, file_2, output)
        self.merge_dialog.exec_()
        if self.merging_state == 2:
            self.signals.show_msg("The video has been downloaded !\nMessage: %s" % log_stream.getvalue().split("\n")
            [-2])

    def convert_handler(self, file_1: str, file_2: str, output: str):
        # subprocess.run(["ffmpeg", "-i", file_1, "-1", file_2, "-crf", "0", "-qscale", "0", output],
        #                capture_output=True, text=True)
        import asyncio
        from ffmpeg import FFmpeg

        # if file_2 is None:
        #     ffmpeg = FFmpeg().input(os.path.join(self.path_preference, file_1).replace("\\", "/")).output(
        #         os.path.join(self.path_preference, output).replace("\\", "/"), {"c:v": "copy", "c:a": "copy"})
        # else:
        ffmpeg = FFmpeg().option("y").input(os.path.join(self.path_preference, file_1).replace("\\", "/")).input(
            os.path.join(
                self.path_preference, file_2).replace("\\", "/")).output(os.path.join(self.path_preference, output)
                                                                         .replace("\\", "/"), {"c:v": "copy",
                                                                                               "c:a": "copy"})

        @ffmpeg.on('start')
        def on_start(arguments):
            logging.log(logging.INFO, 'Starting merge with arguments: ' + str(arguments))

        @ffmpeg.on('stderr')
        def on_stderr(line):
            logging.log(logging.INFO, str(line))

        # @ffmpeg.on('progress')
        # def on_progress(progress):
        #     print(progress)

        @ffmpeg.on('progress')
        def time_to_terminate(progress):
            # Gracefully terminate when more than 200 frames are processed
            # if progress.frame > 200:
            #     ffmpeg.terminate()
            pass

        @ffmpeg.on('completed')
        def on_completed():
            logging.log(logging.INFO, "Completed !")
            main_window.merging_state = 2

        @ffmpeg.on('terminated')
        def on_terminated():
            logging.log(logging.CRITICAL, "Terminated !")

        @ffmpeg.on('error')
        def on_error(code):
            logging.log(logging.CRITICAL, "FATAL ERROR: " + str(code))
            self.merging_state = 3
            with open(os.path.join(str(pathlib.Path.home()), "YouTubeDownloader_CRASH.txt"), "w+") as file:
                file.write(log_stream.getvalue())
                file.close()
            self.signals.show_msg("An error has been detected and merging was probably unsuccessful !\nThe log file has"
                                  " been added to your home folder.", "error")

        loop = asyncio.new_event_loop()
        loop.run_until_complete(ffmpeg.execute())
        loop.close()

    def closeEvent(self, event):
        should_close = True
        try:
            if self.is_download_thread_alive:
                msgbox = QMessageBox(parent=main_window)
                msgbox.setIcon(QMessageBox.Question)
                msgbox.setWindowTitle("Youtube Downloader by Nicklor")
                msgbox.setText("Background download is running.\nDo you want to stop, cancel or continue downloading "
                               "in background ?")
                msgbox.setStandardButtons(QMessageBox.Discard | QMessageBox.Yes | QMessageBox.Cancel |
                                          QMessageBox.Ignore)
                cancel_dl_btn = msgbox.button(QMessageBox.Discard)
                cancel_dl_btn.setText("Cancel Download and close")
                stop_dl_btn = msgbox.button(QMessageBox.Yes)
                stop_dl_btn.setText("Stop Download and close")
                continue_dl = msgbox.button(QMessageBox.Ignore)
                continue_dl.setText("Continue Download in background and close")
                cancel_close_btn = msgbox.button(QMessageBox.Cancel)
                cancel_close_btn.setText("Cancel close")
                msgbox.exec_()
                if msgbox.clickedButton() == cancel_close_btn:
                    should_close = False
                elif msgbox.clickedButton() == cancel_dl_btn:
                    self.cancel_download()
                elif msgbox.clickedButton() == stop_dl_btn:
                    try:
                        self.thread_listen_bar.kill()
                    except Exception as e:
                        logging.log(logging.ERROR, str(e))
                    try:
                        self.thread_download_vid.kill()
                    except Exception as e:
                        logging.log(logging.ERROR, str(e))
                    try:
                        self.thread_download_aud.kill()
                    except Exception as e:
                        logging.log(logging.ERROR, str(e))
        except Exception as e:
            logging.log(logging.ERROR, str(e))
        if not should_close:
            event.ignore()
        else:
            event.accept()

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
        self.checkBox_3.clicked.connect(self.checkbox_3_check)
        self.actionAsk_what_to_do.triggered.connect(lambda: self.qactions(2))
        self.actionReplace_file.triggered.connect(lambda: self.qactions(3))
        self.actionSkip_download.triggered.connect(lambda: self.qactions(4))
        self.cancelDownloadButton.clicked.connect(self.cancel_download)
        self.actionAbout_Qt.triggered.connect(app.aboutQt)
        self.actionSystem.triggered.connect(lambda: self.change_theme("system"))
        self.actionFusion.triggered.connect(lambda: self.change_theme("fusion"))
        self.actionDark_Fusion.triggered.connect(lambda: self.change_theme("dark_fusion"))
        self.actionDark_Orange.triggered.connect(lambda: self.change_theme("darkorange"))
        self.actionOld_Windows.triggered.connect(lambda: self.change_theme("windows"))
        self.actionLight_Material.triggered.connect(lambda: self.change_theme("light_material"))
        self.actionDark_Material.triggered.connect(lambda: self.change_theme("dark_material"))

    def change_theme(self, theme: str):
        self.theme_actions_mgr()
        self.signals.show_msg("You need to restart the app to apply changes !")
        save_theme(theme)

    def theme_actions_mgr(self):
        self.actionSystem.setChecked(False)
        self.actionOld_Windows.setChecked(False)
        self.actionFusion.setChecked(False)
        self.actionDark_Fusion.setChecked(False)
        self.actionDark_Orange.setChecked(False)
        self.actionLight_Material.setChecked(False)
        self.actionDark_Material.setChecked(False)
        if selected_theme == "system":
            self.actionSystem.setChecked(True)
        elif selected_theme == "fusion":
            self.actionFusion.setChecked(True)
        elif selected_theme == "dark_fusion":
            self.actionDark_Fusion.setChecked(True)
        elif selected_theme == "darkorange":
            self.actionDark_Orange.setChecked(True)
        elif selected_theme == "windows":
            self.actionOld_Windows.setChecked(True)
        elif selected_theme == "light_material":
            self.actionLight_Material.setChecked(True)
        elif selected_theme == "dark_material":
            self.actionDark_Material.setChecked(True)

    def checkbox_3_check(self):
        if self.checkBox_3.isChecked():
            self.conv_settings[0] = True
        else:
            self.conv_settings[0] = False
        save_conv_settings(self.conv_settings)

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
            # import tkinter.messagebox
            # import tkinter
            # win = tkinter.Tk()
            # win.withdraw()
            # tkinter.messagebox.showerror("Error", str(e))
            # win.destroy()
            self.signals.show_msg(str(e), "error")
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
            thread = KThread(target=self.download)
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
        if self.checkBox.checkState() and self.checkBox_2.checkState():
            self.checkBox_3.setEnabled(True)
        else:
            self.checkBox_3.setEnabled(False)
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

    def check_if_exists(self, video_name):
        if os.path.isfile(os.path.join(self.path_preference, video_name)):
            return True
        return False

    def download_handler(self):
        self.cancelDownloadButton.show()
        self.clearButton.setDisabled(True)
        self.commandLinkButton.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.SubmitButton.setDisabled(True)
        self.delButton.setDisabled(True)
        self.widget.setDisabled(True)
        self.widget_2.setDisabled(True)
        self.checkBox.setDisabled(True)
        self.checkBox_2.setDisabled(True)
        self.listWidget.setDisabled(True)
        self.listWidget_2.setDisabled(True)
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
                self.thread_download_vid = KThread(target=self.dl_thread, args=(
                    self.ys.filter(type='video').order_by("resolution").desc().first(), prefix,))
                self.thread_download_vid.start()
                self.thread_listen_bar = KThread(target=self.bar_update_thread, args=(
                    self.ys.filter(type='video').order_by("resolution").desc().first().filesize,))
                self.thread_listen_bar.start()
            else:
                self.thread_download_vid = KThread(target=self.dl_thread, args=(
                    self.ys.get_by_itag(self.vid_select_itag), prefix,))
                self.thread_download_vid.start()
                self.thread_listen_bar = KThread(target=self.bar_update_thread, args=(self.ys.get_by_itag(
                    self.vid_select_itag).filesize,))
                self.thread_listen_bar.start()
        elif self.dl_mode == 3:
            if self.bestresbtn_2.isChecked():
                self.thread_download_aud = KThread(target=self.dl_thread, args=(
                    self.ys.filter(type='audio').order_by("abr").desc().first(), "",))
                self.thread_download_aud.start()
                self.thread_listen_bar = KThread(target=self.bar_update_thread, args=(
                    self.ys.filter(type='audio').order_by("abr").desc().first().filesize, "audio",))
                self.thread_listen_bar.start()
            else:
                self.thread_download_aud = KThread(target=self.dl_thread, args=(
                    self.ys.get_by_itag(self.aud_select_itag), "",))
                self.thread_download_aud.start()
                self.thread_listen_bar = KThread(target=self.bar_update_thread, args=(self.ys.get_by_itag(
                    self.aud_select_itag).filesize, "audio",))
                self.thread_listen_bar.start()

    def dl_thread(self, ys, prefix):
        self.is_download_thread_alive = True
        self.currentDownloadName = prefix + ys.default_filename
        ys.download(output_path=self.path_preference, filename_prefix=prefix)
        self.is_download_thread_alive = False

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
                self.signals.use_signal_str("main_window.progressBar.setMaximum(1000)")
                if not (to_update < 0 or to_update > 1000):
                    self.signals.use_signal_int(to_update)
            except Exception as e:
                logging.log(logging.ERROR, str(e))
                self.signals.use_signal_str("main_window.progressBar.setMaximum(0)")
        logging.log(logging.INFO, "Download finished !")
        self.signals.use_signal_str("main_window.progressBar.setMaximum(1000)")
        self.signals.use_signal_int(999)
        if self.dl_mode == 1 or self.dl_mode == 3:
            self.on_dl_finish()
        elif self.dl_mode == 2:
            _type = "audio"
            file_1 = self.currentDownloadName
            if self.bestresbtn_2.isChecked():
                self.thread_download_aud = KThread(target=self.dl_thread, args=(
                    self.ys.filter(type='audio').order_by("abr").desc().first(), "audio_",))
                self.thread_download_aud.start()

            else:
                self.thread_download_aud = KThread(target=self.dl_thread, args=(
                    self.ys.get_by_itag(self.aud_select_itag), "audio_",))
                self.thread_download_aud.start()
            while check_if_alive():
                time.sleep(0.1)
                try:
                    to_update = int((1 - (int(log_stream.getvalue().split("\n")[-2]
                                              .split("download remaining: ")[-1])) / filesize) * 1000)
                    self.signals.use_signal_str("main_window.progressBar.setMaximum(1000)")
                    if not (to_update < 0 or to_update > 1000):
                        self.signals.use_signal_int(to_update)
                except Exception as e:
                    logging.log(logging.ERROR, str(e))
                    self.signals.use_signal_str("main_window.progressBar.setMaximum(0)")
            logging.log(logging.INFO, "Download Finished !")
            if self.conv_settings[0]:
                self.signals.use_signal_str("main_window.show_dialog('%s', '%s', '%s')" % (
                    file_1, self.currentDownloadName, (os.path.splitext(file_1)[0] + ".mp4").split("video_")[1]))
                self.on_dl_finish(False)
            else:
                self.on_dl_finish()

    def qactions(self, num):
        if num == 1:
            path_dialog = PathDialog(self)
            path_dialog.exec_()

        if num == 2:
            self.actionAsk_what_to_do.setChecked(True)
            self.actionReplace_file.setChecked(False)
            self.actionSkip_download.setChecked(False)
            self.conv_settings[2] = 0
            save_conv_settings(self.conv_settings)

        if num == 3:
            self.actionAsk_what_to_do.setChecked(False)
            self.actionReplace_file.setChecked(True)
            self.actionSkip_download.setChecked(False)
            self.conv_settings[2] = 1
            save_conv_settings(self.conv_settings)

        if num == 4:
            self.actionAsk_what_to_do.setChecked(False)
            self.actionReplace_file.setChecked(False)
            self.actionSkip_download.setChecked(True)
            self.conv_settings[2] = 2
            save_conv_settings(self.conv_settings)

    def show_convert_dialog(self):
        convert_dialog = ConvertDialog(self)
        convert_dialog.exec_()

    def cancel_download(self):
        self.cancelDownloadButton.hide()
        self.clean()
        try:
            self.thread_download_aud.kill()
        except Exception as e:
            logging.log(logging.ERROR, str(e))
        try:
            self.thread_download_vid.kill()
        except Exception as e:
            logging.log(logging.ERROR, str(e))
        try:
            self.thread_listen_bar.kill()
        except Exception as e:
            logging.log(logging.ERROR, str(e))
        try:
            time.sleep(2)
            os.remove(os.path.join(self.path_preference, self.currentDownloadName))
        except Exception as e:
            logging.log(logging.ERROR, str(e))

        logging.log(logging.WARN, "Download canceled by user !")
        self.on_dl_finish()

    def on_dl_finish(self, show=True):
        self.signals.use_signal_str("main_window.cancelDownloadButton.hide()")
        self.signals.use_signal_str("main_window.progressBar.setMaximum(1000)")
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
        if self.checkBox.isChecked() and self.chooseresbtn.isChecked():
            self.signals.use_signal_str("main_window.listWidget.setDisabled(False)")
        if self.checkBox_2.isChecked() and self.chooseresbtn_2.isChecked():
            self.signals.use_signal_str("main_window.listWidget_2.setDisabled(False)")
        if show:
            self.signals.show_msg("The video has been downloaded !\nMessage: %s" % log_stream.getvalue().split("\n")
            [-2])


def log_listen_thread():
    while True:
        with open("log.txt", "w+") as log:
            log.write(log_stream.getvalue())
            log.close()
        time.sleep(2)


log_thread = KThread(target=log_listen_thread)
log_thread.start()

app = QApplication(sys.argv)

app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

set_style(app, selected_theme)

main_window = MainWindow()

main_window.show()

exit_code = app.exec_()

log_thread.kill()
with open("log.txt", "w+") as log:
    log.write(log_stream.getvalue())
    log.close()

sys.exit(exit_code)
