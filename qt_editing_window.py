import sys
import typing
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, 
                             QAction,
                             QToolBar, 
                             QMainWindow, 
                             QWidget, 
                             QLabel, 
                             QStatusBar,
                             QListWidget,
                             QLineEdit,
                             QTabWidget,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QPushButton)

class ImgListWidget(QListWidget):
    def __init__(self):
        super().__init__()

class ReviewWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.tab_imageview = QWidget()
        self.tab_globalview = QWidget()

        self.addTab(self.tab_imageview, "图像预览")
        self.addTab(self.tab_globalview, "全局预览")

        self.test_title = QLabel("Test test test")
        self.tab_imageview.layout = QVBoxLayout()
        self.image_label_imageview = QLabel()
        self.image_label_imageview.setPixmap(QPixmap("./resources/images/testimg.png"))
        self.button_edit_image = QPushButton("编辑图像")
        
        self.tab_imageview.layout.addWidget(self.image_label_imageview)
        self.tab_imageview.layout.addWidget(self.test_title)
        
        self.tab_imageview.layout.addWidget(self.button_edit_image)
        self.tab_imageview.setLayout(self.tab_imageview.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PicTools")

        # The toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        # Add image button on the toolbar
        self.add_image_action = QAction(QIcon("./resources/icons/image--plus.png"), "添加图像", self)
        self.add_image_action.setStatusTip("增加一张图像到拼图中。")
        self.add_image_action.triggered.connect(self.onAddImageButtonClick)
        toolbar.addAction(self.add_image_action)


        # The button to enter individual functions
        self.image_list = ImgListWidget()
        self.image_list.addItem("Test item 1")


        # The left side layout
        layout_left = QVBoxLayout()
        layout_left.addWidget(self.image_list)

        # The right side layout
        preview_window = ReviewWidget()

        # The horizontal layout (main of the app)
        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left)
        layout_main.addWidget(preview_window)


        # The container
        container = QWidget()
        container.setLayout(layout_main)

        # Set the central widget of the Window
        self.setCentralWidget(container)

        # Add a status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def onAddImageButtonClick(self):
        print("Click")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()