import sys
import typing
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, 
                             QAction,
                             QToolBar, 
                             QMainWindow, 
                             QWidget, 
                             QLabel, 
                             QStatusBar,
                             QListWidget,
                             QAbstractItemView,
                             QLineEdit,
                             QListWidgetItem,
                             QScrollArea,
                             QTabWidget,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QPushButton)

class ScrollImage(QScrollArea):
    def __init__(self, image : QPixmap):
        super().__init__()
        self.image_label = QLabel()
        self.image_label.setPixmap(image)
        self.setWidget(self.image_label)
    
    def setPixmap(self, image : QPixmap):
        self.image_label.setPixmap(image)

class AspectLockedLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.pixmap = None

    def setImage(self, image : QPixmap):
        self.pixmap = image
        self.setPixmap(image)

    def rescaledPixmap(self):
        return self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event):
        if self.pixmap!= None:
            self.setPixmap(self.rescaledPixmap())

class ImgListItem(QWidget):
    def __init__(self, image : QPixmap, upper_text : str, lower_text : str):
        super().__init__()
        self.pic_label = AspectLockedLabel()
        self.upper_label = QLabel()
        self.lower_label = QLabel()

        self.pic_label.setImage(image)
        self.upper_label.setText(upper_text)
        self.lower_label.setText(lower_text)

        self.label_layout = QVBoxLayout()
        self.overall_layout = QHBoxLayout()
        
        self.label_layout.addWidget(self.upper_label)
        self.label_layout.addWidget(self.lower_label)
        self.overall_layout.addWidget(self.pic_label, 20)
        self.overall_layout.addLayout(self.label_layout, 80)
        self.setLayout(self.overall_layout)

    def setPixmap(self, image : QPixmap):
        self.pic_label.setPixmap(QPixmap)

    def setUppertext(self, text : str):
        self.upper_label.setText(text)

    def setLowertext(self, text : str):
        self.lower_label.setText(text)

class ImgListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)

    def addImageItem(self, image_item : ImgListItem):
        item = QListWidgetItem()
        item.setSizeHint(QSize(200, 150))
        self.addItem(item)
        self.setItemWidget(item, image_item)

class ReviewWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.tab_imageview = QWidget()
        self.tab_globalview = QWidget()

        self.addTab(self.tab_imageview, "图像预览")
        self.addTab(self.tab_globalview, "全局预览")

        # Image view tab
        self.test_title = QLabel("Test test test")
        self.tab_imageview.layout = QVBoxLayout()
        self.image_label_imageview = QLabel()
        self.image_label_imageview.setPixmap(QPixmap("./resources/images/testimg.png"))
        self.button_edit_image = QPushButton("编辑图像")
        self.button_edit_image.setIcon(QIcon("./resources/icons/ruler--pencil.png"))
        
        self.tab_imageview.layout.addWidget(self.image_label_imageview)
        self.tab_imageview.layout.addWidget(self.test_title)
        self.tab_imageview.layout.addWidget(self.button_edit_image)
        self.tab_imageview.setLayout(self.tab_imageview.layout)

        # Global view tab
        self.test_title_global = QLabel("Test test test")
        self.tab_globalview.layout = QVBoxLayout()
        self.image_label_globalview = ScrollImage(QPixmap("./resources/images/testimg.png"))
        self.button_edit_global = QPushButton("编辑设定")
        self.button_edit_global.setIcon(QIcon("./resources/icons/wrench--pencil.png"))
        self.button_export = QPushButton("导出图像")
        self.button_export.setIcon(QIcon("./resources/icons/image-export.png"))

        self.tab_globalview.layout.addWidget(self.image_label_globalview)
        self.tab_globalview.layout.addWidget(self.test_title_global)
        self.tab_globalview.layout.addWidget(self.button_edit_global)
        self.tab_globalview.layout.addWidget(self.button_export)
        self.tab_globalview.setLayout(self.tab_globalview.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PicTools")
        self.setMinimumSize(QSize(1000, 500))

        # The toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        # Add image button on the toolbar
        self.add_image_action = QAction(QIcon("./resources/icons/image--plus.png"), "添加图像", self)
        self.add_image_action.setStatusTip("增加一张图像到拼图中。")
        self.add_image_action.triggered.connect(self.onAddImageButtonClick)
        self.del_image_action = QAction(QIcon("./resources/icons/image--minus.png"), "删除图像", self)
        self.del_image_action.setStatusTip("从拼图中删除当前图像。")
        self.del_image_action.triggered.connect(self.onDelImageButtonClick)
        toolbar.addAction(self.add_image_action)
        toolbar.addAction(self.del_image_action)


        # The button to enter individual functions
        self.image_list = ImgListWidget()
        self.image_list.addImageItem(ImgListItem(QPixmap("./sample_pic/1.jpg"), "1.jpg", "the first image"))
        self.image_list.addImageItem(ImgListItem(QPixmap("./sample_pic/2.jpg"), "2.jpg", "the second image"))
        self.image_list.addImageItem(ImgListItem(QPixmap("./sample_pic/3.jpg"), "3.jpg", "the third image"))
        self.image_list.addImageItem(ImgListItem(QPixmap("./sample_pic/4.jpg"), "4.jpg", "the fourth image"))
        self.image_list.addImageItem(ImgListItem(QPixmap("./sample_pic/center_bg.jpg"), "center.jpg", "the central image"))




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

    def onDelImageButtonClick(self):
        print("Delete")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()