#!/usr/bin/env python3
import subprocess
import sys
import time
import datetime
from PyQt5 import QtGui, QtWidgets
import threading

WAKEUP_HOUR=7
WAKEUP_MINUTE=0

def cancelHibernate():
    print("cancelHibernate")

def runHibernate():
    print("runHibernate")
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    scheduled_datetime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, WAKEUP_HOUR, WAKEUP_MINUTE, 0, 0)
    # scheduled_datetime = datetime.datetime(tomorrow.year, tomorrow.month, 25, 18, 40, 0, 0)
    print("newt wakeup time: %s" % scheduled_datetime)
    unix_time = int(time.mktime(scheduled_datetime.timetuple()))
    res = subprocess.run(["sudo", "rtcwake", "-m", "disk", "-t", str(unix_time)], stdout=subprocess.PIPE)
    sys.stdout.buffer.write(res.stdout)
    print("end runHibernate")

class NotificationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        subject = "Are you sure you want to hibernate your computer now?"
        self.message = "If you do nothing, the computer will hibernate automatically in %s seconds."
        self.setWindowTitle("Notification")

        # subject
        subject_label = QtWidgets.QLabel(subject)
        font = QtGui.QFont()
        font.setBold(True)
        subject_label.setFont(font)
        subject_label_hbox = QtWidgets.QHBoxLayout()
        subject_label_hbox.addWidget(subject_label)

        # message
        self.message_label = QtWidgets.QLabel("")
        message_label_hbox = QtWidgets.QHBoxLayout()
        message_label_hbox.addWidget(self.message_label)

        # button
        self.btn_ok = QtWidgets.QPushButton('Hibernate')
        self.btn_ok.clicked.connect(self.click_ok_button)
        self.btn_ok.setStyleSheet("background-color:#16A085; color:white")
        self.btn_cancel = QtWidgets.QPushButton('Cancel')
        self.btn_cancel.clicked.connect(self.click_cancel_button)
        button_hbox = QtWidgets.QHBoxLayout()
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.btn_cancel)
        button_hbox.addWidget(self.btn_ok)

        # layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(subject_label_hbox)
        vbox.addLayout(message_label_hbox)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)        
        self.setLayout(vbox)    

        # count
        self.start_count_down()
    
    def closeEvent(self, event):
        self.is_closed_window = True

    def start_count_down(self):
        def count_down():
            seconds_remain = 10
            while(not self.is_closed_window):
                if seconds_remain==-1:
                    self.click_ok_button()
                    break
                self.message_label.setText(self.message % str(seconds_remain))
                seconds_remain = seconds_remain-1
                print(seconds_remain)
                time.sleep(1)
            print("end loop")
        self.is_closed_window = False
        self.count_thread = threading.Thread(target=count_down)
        self.count_thread.start()

    def close_window(self):
        self.close()
        self.is_closed_window = True

    def click_cancel_button(self):
        self.close_window()
        cancelHibernate()

    def click_ok_button(self):
        self.close_window()
        runHibernate()
        

if __name__ == "__main__":
    print("start hybernate-and-resume")
    app=QtWidgets.QApplication(sys.argv)
    window=NotificationWindow()
    window.show()
    app.exec_()
    print("end hybernate-and-resume")

