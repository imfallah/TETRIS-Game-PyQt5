from PyQt5 import uic, QtTest
from PyQt5 import uic, QtGui, QtCore, QtTest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from speaker import Speaker
import tetris
import sys
import os
from PyQt5.QtCore import (QPoint,Qt)
from PyQt5.QtCore import *



class LauncherWindow(QDialog):
    def __init__(self):
        super(LauncherWindow, self).__init__()
        uic.loadUi("E:/project/Tetris-game/game/UI/Launcher.ui", self)

        self.setWindowTitle("PyQt5 Tetris")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.show()
        #-----------------
        self.buttonLaunch = self.findChild(QPushButton, "LaunchButton")
        self.buttonUpdate = self.findChild(QPushButton, "CheckUpdatesButton")
        self.buttonExit = self.findChild(QPushButton, "ExitButton")
        #-----------------========
        self.buttonLaunch.clicked.connect(self.LaunchPress)
        self.buttonUpdate.clicked.connect(self.UpdatePress)
        self.buttonExit.clicked.connect(self.ExitPress)
        self.btn_close.clicked.connect(self.close_app)
        self.btn_maximize.clicked.connect(self.maximize_app)
        self.btn_minimize.clicked.connect(self.minimize_app)
        #-----------------========
        self.buttonExit.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonUpdate.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonLaunch.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        #-----------------
        #self.versionText = self.findChild(QLabel, "VersionText")
        #self.versionText.setText("ver. " + self.getLocalVersion())



    def mousePressEvent(self, evt):
        # Handle mouse press event
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        # Handle mouse move event (dragging the window)
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos() 
    def close_app(self):
        self.close()

    def maximize_app(self):
        if self.isMaximized():
            self.showNormal()  # اگر پنجره بزرگ شده بود به حالت نرمال برگردد
        else:
            self.showMaximized()

    def minimize_app(self):
        self.showMinimized()    
        
        
        
        
    def showLauncher(self):
        self.show()
        self.game.hide()
        self.smoothTransform(630, 360)

    def LaunchPress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.smoothTransform(360, 480)
        self.hide()
        self.game = tetris.launchGame()
        self.game.closed.connect(self.showLauncher)

    def UpdatePress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.msgBox = QMessageBox(QMessageBox.Information, "Unavailable", "This feature is currently unavailable", QMessageBox.Ok)
        self.msgBox.exec()

    def ExitPress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_back))
        app.quit()

    def getLocalVersion(self):
        try:
            version_file = open("version.txt")
            version = version_file.readline()
            return version
        except OSError:
            print("could not open version file (OSError)")
            return None

    def smoothTransform(self, width, height): 
        old_h = self.height()
        old_w = self.width()
        end_x = round(self.x() + ((self.width() - width)/2))
        end_y = round(self.y() + ((self.height() - height)/2))
        tick_duration = 20 #minimal tick duration in ms (one frame when transforming the window) 
        prevH = 9998
        prevW = 9998
        x = self.x()
        y = self.y()
        i = 0
        while not (self.height() == height and self.width() == width):
            i+=1
            diff_h = (height - self.height())/9
            diff_w = (width - self.width())/9
            offset_w = old_w - self.width()
            offset_h = old_h - self.height()
            new_x = round(x + (offset_w/2))
            new_y = round(y + (offset_h/2))
            self.move(new_x, new_y)
            if(i%2==0):Speaker.scroll() #play scrolling sound on every second frame
            if(prevW != diff_w or prevH != diff_h):
                prevW = diff_w
                prevH = diff_h
                self.setFixedHeight(round(self.height() + diff_h))
                self.setFixedWidth( round(self.width() + diff_w))
            else:
                self.move(end_x, end_y)
                self.setFixedHeight(height)
                self.setFixedWidth(width)
                break
            QtTest.QTest.qWait(tick_duration)

#=================================##=================================#

app = QApplication(sys.argv)
launcher = LauncherWindow()
app.exec_()

#=================================##=================================#
