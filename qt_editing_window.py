import sys
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt5.QtWidgets import (QApplication, 
                             QAction,
                             QToolBar, 
                             QMainWindow, 
                             QFileDialog,
                             QWidget, 
                             QLabel, 
                             QStatusBar,
                             QListWidget,
                             QAbstractItemView,
                             QLineEdit,
                             QDockWidget,
                             QSplitter,
                             QListWidgetItem,
                             QScrollArea,
                             QTabWidget,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QMessageBox,
                             QPushButton)
from Picture import Picture

developer = "paul-zz"
version = "0.01b"

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
        self.picture_data = image
        self.pic_label = AspectLockedLabel()

        self.upper_label = QLabel()
        font = self.upper_label.font()
        font.setBold(True)
        self.upper_label.setFont(font)

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
        self.pic_label.setPixmap(image)

    def setUppertext(self, text : str):
        self.upper_label.setText(text)

    def setLowertext(self, text : str):
        self.lower_label.setText(text)

class ImgListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def addImageItem(self, image_item : ImgListItem, data : Picture):
        item = QListWidgetItem()
        # Attach data to the item
        item.setSizeHint(QSize(200, 150))
        item.setData(Qt.UserRole, data)
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
        self.image_label_imageview = AspectLockedLabel()
        self.image_label_imageview.setImage(QPixmap("./resources/images/testimg.png"))
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
        self.setWindowIcon(QIcon("./resources/icons/image-instagram.png"))
        self.setMinimumSize(QSize(1000, 500))

        # The menu bar
        menubar = self.menuBar()
        menu_file = menubar.addMenu("文件")
        action_open = menu_file.addAction("打开")
        action_open.setIcon(QIcon("./resources/icons/folder-open-document-text.png"))
        action_save = menu_file.addAction("保存")
        action_save.setIcon(QIcon("./resources/icons/disk.png"))
        action_save.setShortcut("Ctrl+S")

        menu_help = menubar.addMenu("帮助")
        action_github = menu_help.addAction("访问GitHub")
        action_github.setIcon(QIcon("./resources/icons/git.png"))
        action_github.triggered.connect(self.onGotoGithubClick)
        action_about = menu_help.addAction("关于")
        action_about.setIcon(QIcon("./resources/icons/information-frame.png"))
        action_about.triggered.connect(self.onAboutActionClick)

        # The toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        # Add image button on the toolbar
        self.add_image_action = QAction(QIcon("./resources/icons/image--plus.png"), "添加图像", self)
        self.add_image_action.setStatusTip("从本地读取图像并添加到拼图中。")
        self.add_image_action.triggered.connect(self.onAddImageButtonClick)
        self.del_image_action = QAction(QIcon("./resources/icons/image--minus.png"), "删除图像", self)
        self.del_image_action.setStatusTip("从拼图中删除当前图像。")
        self.del_image_action.triggered.connect(self.onDelImageButtonClick)
        toolbar.addAction(self.add_image_action)
        toolbar.addAction(self.del_image_action)

        # Left side : an image list
        self.image_list = ImgListWidget()
        self.image_list.itemSelectionChanged.connect(self.currentImageItemChanged)

        # Right side : preview window
        self.preview_widget = ReviewWidget()
        self.preview_window = QDockWidget("预览窗口", self)
        self.preview_window.setWidget(self.preview_widget)

        # Set central widgete to the image list and add the preview window as dock
        self.setCentralWidget(self.image_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.preview_window)

        # Add a status bar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def onAddImageButtonClick(self):
        # Add image from local folder to the list
        file_info = QFileDialog.getOpenFileNames(self, "选择图片", "./", "图像文件 (*.jpg *.jpeg *.png)")
        file_names = file_info[0]
        for filename in file_names:
            if filename != '':
                pic_data = Picture()
                pic_data.load_image(filename)
                default_name = pic_data.pic_name
                new_image = ImgListItem(QPixmap(filename), filename, default_name)
                self.image_list.addImageItem(new_image, pic_data)

    def onDelImageButtonClick(self):
        # Delete the current image in the image list
        current_item = self.image_list.currentItem()
        self.image_list.takeItem(self.image_list.row(current_item))

    def currentImageItemChanged(self):
        # Refresh the preview window when image clicked
        current_picture = self.image_list.currentItem().data(Qt.UserRole)
        preview_image = current_picture.get_Qt_preview_image()
        picture_name = current_picture.pic_name
        self.preview_widget.image_label_imageview.setImage(preview_image)
        self.preview_widget.test_title.setText(picture_name)

    def onGotoGithubClick(self):
        # Go to the github repository
        QDesktopServices.openUrl(QUrl("https://github.com/paul-zz/WechatLongPic/"))

    def onAboutActionClick(self):
        # Show the about dialogue
        about_dlg = QMessageBox()
        about_dlg.setWindowIcon(QIcon("./resources/icons/information-frame.png"))
        about_dlg.setWindowTitle("关于")
        about_dlg.setText(f"微信朋友圈指定缩略图长图生成器\n开发者: {developer} \n版本: {version}")
        about_dlg.setIcon(QMessageBox.Information)
        about_dlg.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()