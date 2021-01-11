# -*- coding: UTF-8 -*-
#############
## Author       : Yizi
## Github       : https://github.com/MESSISH
## Date         : 2020-04-18 19:35:58
## LastEditors  : Yizi
## LastEditTime : 2021-01-11 15:55:59
## Description  : HDRI管理器
## 以能用为前提创建，结果随着反馈一直到现在瞎jb修了各种bug，如发现还有bug请提交问题XD
## FilePath     : \git_OSS\Houdini\scripts\python\hdri_browser\hdri_browser.py
#############
'''
Houdini中导入的代码

from hdri_browser import hdri_browser as hdri
reload(hdri)
hdri.show()

'''
#? 导入包和模块
import hou
import pdg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import shutil
import ntpath
import time
from threading import Timer
import subprocess
from PySide2 import QtWidgets,QtCore,QtGui,QtUiTools
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

#? 创建类调用
class HWindows(QWidget):
    def __init__(self,parent=None):
        super(HWindows, self).__init__()

        #? 创建文件夹
        self.scripts_path = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
        if not os.path.exists(self.scripts_path +"/HDRI_Path"):
            os.mkdir(self.scripts_path +"/HDRI_Path")

        #? load hdr_path
        try:
            hdrfile = open(self.scripts_path + "/HDRI_Path/hdri_browser_path.txt",'r+')
            txt = hdrfile.readline()
            hdrfile.close()
            self.hdri = txt
            self.temp = "0";
        except (SyntaxError,IOError):
            hdrfile = open(self.scripts_path + "/HDRI_Path/hdri_browser_path.txt",'w+')
            hdrfile.close()
            self.hdri = ""
            self.temp = "0";

        #? load render.txt
        try:
            render = open(self.scripts_path + "/HDRI_Path/render.txt",'r+')
            rendertest = render.readline()
            render.close()
            self.renderfile = rendertest
            if len(rendertest) < 1 :
                self.renderwirt()
        except (SyntaxError,IOError):
            self.renderwirt()

        #? load UI File
        self.ui = QUiLoader().load(self.scripts_path + "/ui/hdri_browser.ui")
        self.InitUI()

    def InitUI(self):
        mainlayout = QVBoxLayout()
        mainlayout.setSpacing(0);
        mainlayout.setContentsMargins(0,0,0,0)
        mainlayout.addWidget(self.ui)

        self.GetWidgets()

        self.setLayout(mainlayout)
        self.setWindowTitle("HDRI Browser")
        self.setIcon()

    def setIcon(self):
        '''
        先创建base64
        with open(r"C:\\Users\\hb\\Downloads\\icon\\1.svg", "rb") as f:  # 用 rb 模式（二进制）打开文件
            image = f.read()
            print(image)  # 打印一下
        '''
        icon= b'<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1609951839422" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1720" xmlns:xlink="http://www.w3.org/1999/xlink" width="128" height="128"><defs><style type="text/css">@font-face { font-weight: 400; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Book-cd7d2bcec649b1243839a15d5eb8f0a3.woff2") format("woff2"); }\n@font-face { font-weight: 500; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Medium-d74eac43c78bd5852478998ce63dceb3.woff2") format("woff2"); }\n@font-face { font-weight: 700; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Bold-83b8ceaf77f49c7cffa44107561909e4.woff2") format("woff2"); }\n@font-face { font-weight: 900; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Black-bf067ecb8aa777ceb6df7d72226febca.woff2") format("woff2"); }\n</style></defs><path d="M512 496c-77.6-60.8-77.6-179.2 0-240 77.6 60.8 77.6 178.4 0 240z" fill="#52DDB2" p-id="1721"></path><path d="M454.4 383.2h-2.4c-12.8-1.6-22.4-13.6-21.6-26.4 5.6-47.2 28.8-89.6 66.4-119.2 10.4-8 25.6-6.4 33.6 4s6.4 25.6-4 33.6c-27.2 21.6-44.8 52-48.8 87.2-0.8 11.2-11.2 20.8-23.2 20.8z" fill="#444B54" p-id="1722"></path><path d="M512 496c-12-98.4 71.2-181.6 169.6-169.6C693.6 424 610.4 508 512 496z" fill="#2B9E7D" p-id="1723"></path><path d="M509.6 496c12-98.4-71.2-181.6-169.6-169.6C328 424 411.2 508 509.6 496z" fill="#FFFFFF" p-id="1724"></path><path d="M531.2 520.8c-6.4 0-13.6 0-20-0.8h-4c-12.8-1.6-22.4-13.6-20.8-26.4v-1.6c0.8-8.8 6.4-16 14.4-20 6.4-2.4 13.6-2.4 20 0.8 37.6 3.2 73.6-10.4 100.8-37.6 23.2-23.2 36.8-53.6 37.6-86.4-27.2 0.8-53.6 10.4-75.2 27.2-7.2 5.6-16 6.4-24 3.2s-13.6-10.4-14.4-19.2c-4-34.4-21.6-64-48-85.6-10.4-8-12-23.2-4-33.6 8-10.4 23.2-12 33.6-4 27.2 21.6 47.2 49.6 58.4 82.4 30.4-15.2 64.8-20.8 99.2-16.8 11.2 1.6 19.2 9.6 20.8 20.8 6.4 54.4-12 107.2-50.4 146.4-33.6 32.8-77.6 51.2-124 51.2zM340.8 393.6c-11.2 0-21.6-8-24-20-2.4-16.8-3.2-33.6-0.8-50.4 1.6-11.2 9.6-19.2 20.8-20.8 48-5.6 95.2 8 132.8 38.4 10.4 8 12 23.2 3.2 33.6-8 10.4-23.2 12-33.6 3.2-22.4-17.6-48.8-28-76-28.8 0 5.6 0.8 11.2 1.6 16.8 2.4 12.8-6.4 25.6-20 27.2-1.6 0.8-2.4 0.8-4 0.8z" fill="#444B54" p-id="1725"></path><path d="M380.8 432c34.4-1.6 67.2 3.2 97.6 13.6 21.6 7.2 45.6 7.2 67.2 0 30.4-9.6 63.2-14.4 97.6-13.6 141.6 5.6 258.4 118.4 268 260C922.4 856 792.8 992 632 992c-43.2 0-84-9.6-120-27.2-36 17.6-76.8 27.2-120 27.2-160.8 0-290.4-136-279.2-299.2C122.4 551.2 239.2 437.6 380.8 432z" fill="#FF5576" p-id="1726"></path><path d="M204 600c-4.8 0-9.6-1.6-14.4-4.8-10.4-8-12.8-23.2-5.6-33.6 38.4-53.6 96-89.6 160-101.6 12.8-2.4 25.6 6.4 28 19.2 2.4 12.8-6.4 25.6-19.2 28-52 9.6-98.4 39.2-129.6 82.4-4 6.4-11.2 10.4-19.2 10.4zM164.8 689.6c-6.4 0-12.8-2.4-16.8-7.2-4.8-4-7.2-10.4-7.2-16.8 0-1.6 0-3.2 0.8-4.8 0-1.6 0.8-3.2 1.6-4.8 0.8-1.6 1.6-3.2 2.4-4 0.8-1.6 1.6-2.4 3.2-4 0.8-0.8 2.4-2.4 4-3.2 1.6-0.8 2.4-1.6 4-2.4 1.6-0.8 3.2-0.8 4.8-1.6 8-1.6 16 0.8 21.6 6.4 0.8 0.8 2.4 2.4 3.2 4 0.8 1.6 1.6 2.4 2.4 4 0.8 1.6 0.8 3.2 1.6 4.8 0 1.6 0.8 3.2 0.8 4.8 0 6.4-2.4 12.8-7.2 16.8-7.2 4.8-12.8 8-19.2 8z" fill="#FFFFFF" p-id="1727"></path><path d="M530.4 972.8c3.2 1.6 6.4 2.4 9.6 4 1.6 0.8 4 0.8 5.6 1.6 3.2 0.8 5.6 1.6 8.8 3.2 2.4 0.8 4 0.8 6.4 1.6 3.2 0.8 5.6 1.6 8.8 2.4 2.4 0.8 4.8 0.8 6.4 1.6 3.2 0.8 5.6 1.6 8.8 1.6 2.4 0 4.8 0.8 7.2 0.8 3.2 0.8 5.6 0.8 8.8 0.8 2.4 0 4.8 0.8 7.2 0.8 3.2 0 5.6 0.8 8.8 0.8h29.6c3.2 0 5.6 0 8.8-0.8h4.8c4-0.8 8-0.8 12.8-1.6h0.8c122.4-18.4 220.8-116.8 236.8-240.8 0.8-3.2 0.8-6.4 0.8-9.6v-4c0-4 0.8-7.2 0.8-11.2 0-9.6 0-20-0.8-30.4-9.6-141.6-124.8-254.4-264.8-260.8C726.4 473.6 792 556.8 792 656c0 141.6-56 264-200 264-40 0-63.2-38.4-88-22.4-44.8 28-95.2 48-152 38.4h-1.6c-50.4 0-58.4 41.6-10.4 51.2 1.6 0 3.2 0.8 4.8 0.8 1.6 0 4 0.8 5.6 0.8 2.4 0.8 5.6 0.8 8.8 0.8 1.6 0 3.2 0.8 5.6 0.8 3.2 0 6.4 0.8 9.6 0.8h18.4c43.2 0 84-9.6 120-27.2 4.8 2.4 8.8 4 13.6 6.4 0.8 1.6 2.4 1.6 4 2.4z" fill="#C95065" p-id="1728"></path><path d="M632 1016c-19.2 0-39.2-1.6-58.4-5.6-40.8-8-83.2-8-124 0-19.2 4-38.4 5.6-58.4 5.6-84 0-164.8-35.2-222.4-96.8-56.8-61.6-85.6-143.2-80-228C99.2 538.4 227.2 414.4 380 408c33.6-1.6 66.4 2.4 97.6 12 6.4 1.6 12 3.2 17.6 4.8 19.2 4.8 41.6 9.6 85.6 32 12 5.6 16.8 20 11.2 32s-20 16.8-32 11.2c-39.2-19.2-57.6-24-76-28-6.4-1.6-12.8-3.2-20-4.8-26.4-8-54.4-11.2-82.4-10.4-128.8 4.8-236.8 109.6-245.6 237.6-4.8 72 19.2 140 68 192.8C253.6 939.2 320 968 392 968c16.8 0 32.8-1.6 48.8-4.8 47.2-8.8 95.2-8.8 142.4 0 16 3.2 32.8 4.8 48.8 4.8 72 0 138.4-28.8 187.2-81.6 48.8-52 72.8-120.8 68-192.8-8.8-128-116-232.8-244.8-237.6-13.6-0.8-23.2-12-23.2-24.8 0.8-13.6 11.2-24 24.8-23.2 152.8 5.6 280.8 130.4 291.2 282.4 5.6 85.6-23.2 166.4-80.8 228.8C796.8 980.8 716 1016 632 1016z" fill="#444B54" p-id="1729"></path><path d="M872 1016H152c-13.6 0-24-10.4-24-24s10.4-24 24-24h720c13.6 0 24 10.4 24 24s-10.4 24-24 24zM992 1016c-1.6 0-3.2 0-4.8-0.8-1.6 0-3.2-0.8-4.8-1.6-1.6-0.8-2.4-1.6-4-2.4-1.6-0.8-2.4-1.6-4-3.2l-3.2-3.2c-0.8-1.6-1.6-2.4-2.4-4-0.8-1.6-0.8-3.2-1.6-4.8 0-1.6-0.8-3.2-0.8-4.8 0-1.6 0-3.2 0.8-4.8 0-1.6 0.8-3.2 1.6-4.8 0.8-1.6 1.6-2.4 2.4-4 0.8-1.6 1.6-2.4 3.2-4s2.4-2.4 4-3.2c1.6-0.8 2.4-1.6 4-2.4 1.6-0.8 3.2-0.8 4.8-1.6 3.2-0.8 6.4-0.8 9.6 0 1.6 0 3.2 0.8 4.8 1.6 1.6 0.8 3.2 1.6 4 2.4 1.6 0.8 2.4 1.6 4 3.2 0.8 0.8 2.4 2.4 3.2 4 0.8 1.6 1.6 2.4 2.4 4 0.8 1.6 0.8 3.2 1.6 4.8 0 1.6 0.8 3.2 0.8 4.8 0 1.6 0 3.2-0.8 4.8 0 1.6-0.8 3.2-1.6 4.8s-1.6 3.2-2.4 4c-0.8 1.6-1.6 2.4-3.2 3.2-4.8 5.6-11.2 8-17.6 8z" fill="#444B54" p-id="1730"></path></svg>'
        icon_get = QPixmap()
        icon_get.loadFromData(icon)
        appIcon = QIcon(icon_get)
        self.setWindowIcon(appIcon)

    def GetWidgets(self):
        """
        设置控件
        """
        #& btn_proj_path加载图标
        image = b'<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1609656219985" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="8030" xmlns:xlink="http://www.w3.org/1999/xlink" width="128" height="128"><defs><style type="text/css">@font-face { font-weight: 400; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Book-cd7d2bcec649b1243839a15d5eb8f0a3.woff2") format("woff2"); }\n@font-face { font-weight: 500; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Medium-d74eac43c78bd5852478998ce63dceb3.woff2") format("woff2"); }\n@font-face { font-weight: 700; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Bold-83b8ceaf77f49c7cffa44107561909e4.woff2") format("woff2"); }\n@font-face { font-weight: 900; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Black-bf067ecb8aa777ceb6df7d72226febca.woff2") format("woff2"); }\n</style></defs><path d="M928 444H820V330.4c0-17.7-14.3-32-32-32H473L355.7 186.2c-1.5-1.4-3.5-2.2-5.5-2.2H96c-17.7 0-32 14.3-32 32v592c0 17.7 14.3 32 32 32h698c13 0 24.8-7.9 29.7-20l134-332c1.5-3.8 2.3-7.9 2.3-12 0-17.7-14.3-32-32-32zM136 256h188.5l119.6 114.4H748V444H238c-13 0-24.8 7.9-29.7 20L136 643.2V256z m635.3 512H159l103.3-256h612.4L771.3 768z" p-id="8031" fill="#dbdbdb"></path></svg>'
        btn_proj_path_icon = QPixmap()
        btn_proj_path_icon.loadFromData(image)


        btn_image = b'<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg t="1610118992486" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2753" xmlns:xlink="http://www.w3.org/1999/xlink" width="128" height="128"><defs><style type="text/css">@font-face { font-weight: 400; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Book-cd7d2bcec649b1243839a15d5eb8f0a3.woff2") format("woff2"); }@font-face { font-weight: 500; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Medium-d74eac43c78bd5852478998ce63dceb3.woff2") format("woff2"); }@font-face { font-weight: 700; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Bold-83b8ceaf77f49c7cffa44107561909e4.woff2") format("woff2"); }@font-face { font-weight: 900; font-style: normal; font-family: Circular-Loom; src: url("https://cdn.loom.com/assets/fonts/circular/CircularXXWeb-Black-bf067ecb8aa777ceb6df7d72226febca.woff2") format("woff2"); }</style></defs><path d="M832 626.592l-128-128-128 128-256.48-256.448L192 497.632V191.872h640V626.56z m0 205.28H192V588.16l127.52-127.52L576 717.12l128-128 128 128v114.72z m0-704H128v768h768v-768h-64z" fill="#dbdbdb" p-id="2754"></path><path d="M672 319.872c-17.632 0-32 14.368-32 32 0 17.6 14.368 32 32 32 17.632 0 32-14.4 32-32 0-17.632-14.368-32-32-32m0 128c-52.928 0-96-43.072-96-96s43.072-96 96-96 96 43.072 96 96-43.072 96-96 96" fill="#dbdbdb" p-id="2755"></path></svg>'
        btn_image_icon = QPixmap()
        btn_image_icon.loadFromData(btn_image )

        btn_proj_path = self.ui.findChild(QPushButton,"proj_path")
        self.btn_creatimg = self.ui.findChild(QPushButton,"creatimg")
        self.cleanimage = self.ui.findChild(QPushButton, "cleanimage")
        self.folderlist = self.ui.findChild(QComboBox, "path_list")
        self.path_info = self.ui.findChild(QLabel, "path_info")
        self.rendererlist = self.ui.findChild(QComboBox,"renderlist")
        self.hdrilist = self.ui.findChild(QListWidget, "hdrilist")


        btn_proj_path.setIcon(btn_proj_path_icon)
        self.btn_creatimg.setIcon(btn_image_icon)
        self.hdrilist.setViewMode(QListView.IconMode)
        self.hdrilist.setIconSize(QSize(150,100))
        self.hdrilist.setResizeMode(QListWidget.Adjust)
        self.path_info.setText(self.hdri)

        self.hdrilist.customContextMenuRequested[QtCore.QPoint].connect(self.ListWidgetContext)
        btn_proj_path.clicked.connect(self.set_hdri_folder)
        if hou.applicationVersionString() > '18.0' :
            self.btn_creatimg.clicked.connect(self.create_image_to_jpg)
        else:
            self.btn_creatimg.clicked.connect(self.version)
        self.cleanimage.clicked.connect(self.delerrorimage)
        self.folderlist.activated.connect(self.Refresh)
        self.folderlist.activated.connect(self.CreateInterface)


        self.renderset()
        self.Refresh()
        self.CreateInterface()

    def renderwirt(self):
        """写入文件
        """
        render = open(self.scripts_path + "/HDRI_Path/render.txt",'w+')
        renderer = "Redshift,Mantra,Arnold,Vray,Octane"
        render.write(renderer)
        render.close()
        self.renderfile = renderer

    def renderset(self):
        """添加render渲染器列表
        """
        rendertext = self.renderfile
        rendersort = rendertext.split(",")
        for render in rendersort:
            self.rendererlist.addItem(render)

    def set_hdri_folder(self):
        """设置hdri文件夹
        """
        setpath = hou.ui.selectFile(title="Set Hdri Path",file_type=hou.fileType.Directory)
        newpath = os.path.dirname(setpath) +"/"
        if (newpath != "/"):
            self.hdri = newpath
            f = open(self.scripts_path + "/HDRI_Path/hdri_browser_path.txt","w+")
            f.write(newpath)
            f.close()

        self.Refresh()
        self.CreateInterface()
        self.path_info.setText(self.hdri)

    def Refresh(self):
        """设置路径
        """
        if self.hdri != self.temp and self.hdri !="":
            self.folderlist.clear()
            for folder in os.listdir(self.hdri):
                full_path = os.path.join(self.hdri, folder)
                if  os.path.isdir(full_path):
                    self.folderlist.addItem(folder)

            self.temp = self.hdri

        self.instexpath = self.hdri + str(self.folderlist.currentText()) + "/Thumbnails/"
        self.texpath = self.hdri + str(self.folderlist.currentText()) + "/HDRIs/"

    def CreateInterface(self):
        """创建缩略图
        """
        self.hdrilist.clear()

        try:
            for file in os.listdir(self.instexpath):
                if file.endswith('.jpg'):
                    file_temp = file.split(".")
                    del file_temp[-1]
                    name = ".".join(file_temp)
                    indextex0 = self.instexpath + file
                    icon = QtGui.QIcon(indextex0)
                    item = QListWidgetItem(icon, "")
                    item.setSizeHint(QSize(155,100))
                    item.setText(name)
                    item.setToolTip('<b>%s</b><br><img src="%s">' % (name, indextex0))
                    self.hdrilist.addItem(item)

        except WindowsError:
            pass

        #! 这里不知道是不是bug问题，还是自己思路错了，会加item传递进去，导致执行多次事件，加了disconnect强制中断事件.
        try: self.hdrilist.clicked.disconnect(self.setTex)
        except Exception: pass
        self.hdrilist.clicked.connect(self.setTex)

        try:self.hdrilist.doubleClicked.disconnect(self.create_node)
        except Exception: pass
        self.hdrilist.doubleClicked.connect(self.create_node)

    def setTex(self,item):
        """节点设置贴图路径

        Args:
            item (index): 传入父类item的数据
        """
        texname = item.data()

        for texture in os.listdir(self.texpath):
                tex = texture.split(texname)
                if len(tex)>=2:
                    texname = texture
        node_path = self.texpath + texname

        try:
            node = hou.selectedNodes()[0]
            light_node = node.parm('env_map')
            if(light_node == None):
                light_node = node.parm('ar_light_color_texture')
                if (light_node == None):
                    light_node = node.parm('A_FILENAME')
                    light_node.set(node_path)
                light_node.set(node_path)
            light_node.set(node_path)

        except AttributeError:
            hou.ui.setStatusMessage ('======================================================================没找到可以放环境贴图参数的位置,============确认下是不是选择错节点了,或者灯光节点没有切换成环境灯光模式.=================如果要创建节点，请保证不要选择节点======================================================================', severity=hou.severityType.Warning)
            t = Timer(5, self.clean_message)
            t.start()
        except IndexError:
            pass

    def create_node(self,item):
        """创建节点并设置贴图

        Args:
            item (index): 传入父类item的数据
        """
        texname = item.data()
        for texture in os.listdir(self.texpath):
                j = texture.split(texname)
                if len(j)>=2:
                    texname = texture

        node_path = self.texpath + texname
        render_name = self.rendererlist.currentText()
        if render_name == "Redshift":
            try:
                rslight = hou.node('/obj/').createNode('rslightdome')
                rslight.setCurrent(True, True)
                rslight.moveToGoodPosition()
                rs_env = rslight.parm('env_map')
                rs_env.set(node_path)

            except hou.OperationFailed:
                hou.ui.setStatusMessage ('==========================好像没安装Redshift渲染器==================没安装是创建不了Redshift环境灯光节点的======================================================================', severity=hou.severityType.Warning)
                t = Timer(5, self.clean_message)
                t.start()
        elif render_name == "Mantra":
            try:
                with hou.undos.group("创建Mantra环境灯光节点"):
                    mtlight = hou.node('/obj/').createNode('envlight')
                    mt_env = mtlight.parm('env_map')
                    mt_env.set(node_path)
                    mtlight.setCurrent(True, True)
                    mtlight.moveToGoodPosition()
                    hou.ui.setStatusMessage ('已成功创建Mantra环境灯光节点' , severity=hou.severityType.Message)
            except:
                hou.ui.displayMessage("这你都能报错？？？\n别弄了赶紧找小的救命",severity=hou.severityType.Error)
        elif render_name == "Arnold":
            try:
                with hou.undos.group("创建Arnold环境灯光节点"):
                    arlight = hou.node('/obj/').createNode('arnold_light')
                    arlight.parm("ar_light_type").set('skydome')
                    arlight.parm("ar_light_color_type").set('texture')
                    arlight.setCurrent(True, True)
                    arlight.moveToGoodPosition()
                    ar_env = arlight.parm('ar_light_color_texture')
                    ar_env.set(node_path)
                    hou.ui.setStatusMessage ('已成功创建Arnold环境灯光节点' , severity=hou.severityType.Message)
            except hou.OperationFailed:
                hou.ui.setStatusMessage ('==========================好像没安装Arnold渲染器==================没安装是创建不了Arnold环境灯光节点的======================================================================', severity=hou.severityType.Warning)
                t = Timer(5, self.clean_message)
                t.start()
        elif render_name == "Vray":
            try:
                with hou.undos.group("创建Vray环境灯光节点"):
                    vrlight = hou.node('/obj/').createNode('VRayNodeLightDome')
                    vrlight.setCurrent(True, True)
                    vrlight.moveToGoodPosition()
                    vr_env = vrlight.parm('dome_tex')
                    vr_env.set(node_path)
                    hou.ui.setStatusMessage ('已成功创建Vray环境灯光节点' , severity=hou.severityType.Message)
                pass
            except hou.OperationFailed:
                hou.ui.setStatusMessage ('==========================好像没安装Vray渲染器==================没安装是创建不了Vray环境灯光节点的======================================================================', severity=hou.severityType.Warning)
                t = Timer(5, self.clean_message)
                t.start()
        elif render_name == "Octane":
            try:
                with hou.undos.group("创建Octane环境灯光节点"):
                    oclight = hou.node('/shop/').createNode('octane_rendertarget_dl')
                    oclight.parm("parmKernel").set('1')
                    oclight.parm("parmEnvironment").set('1')
                    oclight.setCurrent(True, True)
                    oclight.moveToGoodPosition()
                    oc_env = oclight.parm('A_FILENAME')
                    oc_env.set(node_path)
                    hou.ui.setStatusMessage ('已成功创建Octane环境灯光节点' , severity=hou.severityType.Message)
            except hou.OperationFailed:
                hou.ui.setStatusMessage ('==========================好像没安装Octane渲染器==================没安装是创建不了Octane环境灯光节点的======================================================================', severity=hou.severityType.Warning)
                t = Timer(5, self.clean_message)
                t.start()
        else:
            hou.ui.displayMessage("目前只支持\n-------Redshift,Vray,Mantra,Arnold-------\n提示报错，请注意在该工具脚本存在位置的HDRI_Path/render.txt里的内容,格式如下\nRedshift,Vray,Mantra,Arnold\n解决不了，就删除render.txt文件，重新打开工具",severity=hou.severityType.Error)

    def create_image_to_jpg(self):
        Directory = self.hdri + self.folderlist.currentText()+'/'
        self.file_Directory = Directory
        hdri_exr = self.check(Directory)
        if hdri_exr == []:
            hou.ui.displayMessage("在%s路径下没找到.hdr或.exr后缀需要生成缩略图的环境贴图"%Directory,severity=hou.severityType.Error)
        else:
            for filename in hdri_exr:
                if filename.split('.')[1] == 'hdr':
                    type = 'hdr'
                    dir = Directory+'*.hdr'
                else :
                    type = 'exr'
                    dir = Directory+'*.exr'
            self.create_top(type,dir)


    def create_top(self,type,dir):
        thdir = self.file_Directory+'/Thumbnails/'
        if not os.path.exists(thdir):
            os.mkdir(thdir)
        hipsave = hou.ui.displayMessage('==========由于此功能是利用PDG进行，需要保存文件备份==============\n==============会调用CPU核心数-1的资源进行缩略图生成==============\n=========在生成完成前，请不要进行其他操作，防止意外发生XD=========\n该功能还有BUG存在(只遇到过一次，找不到原因，不知道怎么再次触发)', buttons=('保存文件后启动','保存到Backup后启动','关闭'), severity=hou.severityType.Warning,default_choice=0,close_choice=2,title='创建PDG进行缩略图生成')
        if hipsave == 0 :
            hou.hipFile.save()
        if hipsave == 1 :
            hou.hipFile.saveAsBackup()
        if hipsave == 0 or hipsave == 1:
            with hou.undos.group("创建top节点进行缩略图生成"):
                hou.ui.setStatusMessage ('==========================正在进行缩略图生成，请不要进行其他操作，防止意外发生==========================', severity=hou.severityType.Fatal)
                top = hou.node('/obj').createNode('topnet','%s_to_jpg'%type)
                top.setComment('    缩略图生成中')
                top.setCurrent(True, True)
                top.moveToGoodPosition()
                group = top.parmTemplateGroup()
                destroy = hou.ButtonParmTemplate('del','自毁',script_callback='hou.pwd().destroy(disable_safety_checks=False)',script_callback_language=hou.scriptLanguage.Python)
                pausee = hou.ButtonParmTemplate('pause','暂停',script_callback='hou.pwd().pauseCook()',script_callback_language=hou.scriptLanguage.Python)
                cancelCook = hou.ButtonParmTemplate('cancelCook','取消',script_callback='hou.pwd().pauseCook()',script_callback_language=hou.scriptLanguage.Python)
                folder = group.findFolder('Scheduler')
                group.appendToFolder(folder,destroy)
                top.setParmTemplateGroup(group)
                top.setGenericFlag(hou.nodeFlag.DisplayComment,True)
                localscheduler = top.children()[0]
                localscheduler.parm('maxprocsmenu').set('-1')
                top_path = top.path()
                filepattern = hou.node(top_path).createNode('filepattern')
                filepattern.parm('pattern').set('%s'%dir)
                attributefromstring = filepattern.createOutputNode('attributefromstring')
                attributefromstring.parm('sourcestring').set('`@filename`')
                attributefromstring.parm('useregex').set('on')
                attributefromstring.parm('matchstring').set('(.+?)\.')
                ropcomposite = attributefromstring.createOutputNode('ropcomposite')
                ropcomposite.parm('tres').set('specify')
                ropcomposite.parm('res1').set('400')
                ropcomposite.parm('res2').set('200')
                ropcomposite.parm('copoutput').set('`@directory`/Thumbnails/`@group0`.jpg')

                ropcomposite.setGenericFlag(hou.nodeFlag.OutputForDisplay, 1)
                ropcomposite.executeGraph(False, False, False,True)
                pdg_node = ropcomposite.getPDGNode()
                pdg_context = ropcomposite.getPDGGraphContext()
                pdg_context.addEventHandler(self.print_done_and_remove, pdg.EventType.CookComplete, True)

                top.layoutChildren()
                top.parm('cookbutton').pressButton()


            return top
    def print_done_and_remove(self,handler, event):
        self.CreateInterface()
        hou.ui.setStatusMessage ('==========================已成功生成缩略图===================在创建的节点上有***自毁***按钮,点击删除节点======================', severity=hou.severityType.Warning)
        hou.ui.displayMessage('=======================已成功生成缩略图=====================\n===在创建的节点上有***自毁***按钮,点击按钮删除节点===', severity=hou.severityType.Message)
        Directory = self.file_Directory
        cheaktype=['hdr','exr']
        t = Timer(5, self.clean_message)
        t.start()

        dir = Directory+'/HDRIs/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        for file in os.listdir(Directory):
            if not (file == 'HDRIs' or file == 'Thumbnails'):
                file_path = os.path.join(Directory,file)
                if file.split('.')[-1] in cheaktype:
                    shutil.move(file_path, dir)

    def version(self):
        hou.ui.displayMessage('=======由于此功能是PDG生成，18.0以上变动太多，只适用于18.0以上的版本(包括18.0)=======\n=====================自行将缩略图400*200放在Thumbnails文件夹内====================\n=================================HDR放在HDRIs内=================================\n=================================右键刷新贴图====================================')

    def check(self,dir):
        filename_list = []
        Thumbnails_list=[]
        HDRIs_list=[]
        check_file = [".hdr",".exr"]

        for root,dir_name,files_name in os.walk(dir):
            if not (os.path.basename(root) == 'HDRIs' and os.path.basename(root) == 'Thumbnails' ):
                for filename in os.listdir(root):
                    if os.path.splitext(filename)[1] in check_file :
                        file_path = os.path.join(root,filename)
                        try:
                            shutil.move(file_path, dir)
                        except shutil.Error:
                            pass
                        filename_list.append(filename)
            try:
                os.rmdir(root)
            except OSError:
                pass


            if os.path.exists(self.instexpath) and os.path.exists(self.texpath) :
                if os.path.basename(root) == 'Thumbnails':
                    for filenamee in os.listdir(root):
                        Thumbnails_list.append(filenamee)

                if os.path.basename(root) == 'HDRIs':
                    for roott,dir_namee,files_namee in os.walk(root):
                        for i in files_namee:
                            HDRIs_list.append(i)
        result_list = self.list_dif(Thumbnails_list,HDRIs_list)
        if len(result_list) > 0:
            for i in result_list:
                filename_list.append(i)
            for root,dir_name,files_name in os.walk(os.path.join(dir,'HDRIs')):
                if (files_name in result_list):
                    if os.path.splitext(files_name)[1] in check_file :
                        file_pathh = os.path.join(root,files_name)
                        try:
                            shutil.move(file_pathh, dir)
                        except shutil.Error:
                            pass
                try:
                    os.rmdir(root)
                except OSError:
                    pass

        while '' in filename_list:
            filename_list.remove('')
        return filename_list




    def list_dif(self,list1,list2):
        t1 = set(list1)
        h1 = set(list2)
        result = h1.difference(t1)
        result_list = list(result)
        return result_list

    def ListWidgetContext(self,point):
        """设置右键菜单

        """
        try:
            index = self.hdrilist.currentIndex()
            file_name = index.data()
            self.fullname = file_name
            self.filename_path = self.texpath + file_name
            if os.path.exists(self.filename_path +'.exr') :
                self.file_path = self.filename_path +'.exr'
            else:
                self.file_path = self.filename_path +'.hdr'
            self.file_jpg =self.instexpath +file_name+".jpg"
            self.file_path_fix = self.file_path.replace('/','\\')
        except TypeError:
            pass
        popMenu = QMenu(self)
        pop_Menu_open_file = popMenu.addAction('打开文件')
        pop_Menu_open_file.triggered.connect(self.open_file)
        pop_Menu_open_file_path = popMenu.addAction('打开文件路径')
        pop_Menu_open_file_path.triggered.connect(self.open_file_path)
        pop_Menu_rename_file_path = popMenu.addAction('重命名')
        pop_Menu_rename_file_path.triggered.connect(self.rename)
        pop_Menu_ref_file_path = popMenu.addAction('刷新')
        pop_Menu_ref_file_path.triggered.connect(self.CreateInterface)
        pop_Menu_del_file_path = popMenu.addAction('删除文件和缩略图')
        pop_Menu_del_file_path.triggered.connect(self.delfile)

        popMenu.exec_(QCursor.pos())



    def open_file(self):
        try:
            os.startfile(self.file_path, 'open')
        except WindowsError:
            try:
                self.file_path = self.file_path.replace('.exr','.hdr')
                os.startfile(self.file_path, 'open')
            except WindowsError:
                hou.ui.displayMessage("缩略图存在，但找不到源文件",severity=hou.severityType.Error)
        except:
            pass


    def open_file_path(self):
        """
        用subprocess可以避免cmd黑色窗口弹出
        """
        try:
            temp = open(self.file_path)
            temp.close()
            subprocess.Popen(r'explorer /select,%s'%self.file_path_fix)
        except IOError:
            self.file_path_fix = self.file_path_fix.replace('.exr','.hdr')
            subprocess.Popen(r'explorer /select,%s'%self.file_path_fix)
        except:
            pass

    def rename(self):
        file_suffix = self.file_path.split('.')[-1]
        i = True
        while i == True:
            i = False
            hou.ui.setStatusMessage ('输入新的文件名称' , severity=hou.severityType .Message )
            inputs = hou.ui.readInput('重命名文件名字',buttons=('确定','关闭'),severity=hou.severityType.Message)
            newname = inputs[1]
            try:
                if inputs[0] == 0 :
                    os.rename(self.file_path,self.texpath+'%s'%newname+'.'+file_suffix)
                    os.rename(self.file_jpg,self.instexpath+'%s'%newname+'.jpg')
                    hou.ui.setStatusMessage ('已重命名' , severity=hou.severityType.Message)
                    self.CreateInterface()
                    t = Timer(3, self.clean_message)
                    t.start()
            except WindowsError:
                if hou.ui.displayMessage("当前文件名字已存在，无法命名",severity=hou.severityType.Error) == 0:
                    i = True
                else:
                    pass
    def delerrorimage(self):
        Thumbnails_list=[]
        HDRIs_list=[]
        cheak = ['hdr','exr']
        if os.path.exists(self.instexpath):
            for image in os.listdir(self.instexpath):
                if image.split('.')[1] == 'jpg':
                    newimage = image.split('.')[0]
                    Thumbnails_list.append(newimage)
        if os.path.exists(self.texpath):
            for hdr in os.listdir(self.texpath):
                if hdr.split('.')[1] in cheak:
                    newhdr = hdr.split('.')[0]
                    HDRIs_list.append(newhdr)

        result_list = self.list_dif(HDRIs_list,Thumbnails_list)
        while '' in result_list:
            result_list.remove('')
        if len(result_list) > 0:
            for rename in result_list:
                image_full_path = os.path.join(self.instexpath,rename+'.jpg')
                os.remove(image_full_path)
        self.CreateInterface()
        hou.ui.setStatusMessage ('============================已清理无效缩略图=====================================', severity=hou.severityType.Message)
        t = Timer(3, self.clean_message)
        t.start()

    def delfile(self):
        try:
            file_suffix = self.file_path.split('.')[-1]
            os.remove(self.texpath+self.fullname+'.'+file_suffix)
            os.remove(self.file_jpg)
            self.CreateInterface()

            hou.ui.setStatusMessage ('==========================已删除文件和缩略图============================', severity=hou.severityType.Message)
            t = Timer(3, self.clean_message)
            t.start()
        except TypeError:
            hou.ui.displayMessage("请选中缩略图再进行操作",severity=hou.severityType.Error)
        except AttributeError:
            hou.ui.displayMessage("请选中缩略图再进行操作",severity=hou.severityType.Error)

    def clean_message(self):
        message = hou.ui.setStatusMessage("")

#? houdini内部显示窗口的方法
def show():
    """
    不用之前的hou.qt.mainWindow()，创建过程中会被python会删除掉pyside2创建过程中的一些变量，必须选择一个存在级别更高的窗口(不确定)
    """
    win = HWindows()
    hou.session.mainWindow = hou.ui.mainQtWindow()
    win.setParent(hou.session.mainWindow, Qt.Window)
    win.show()
