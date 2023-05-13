import sys
from PyQt5.QtCore import QSize, Qt, QUrl, QT_VERSION_STR, PYQT_VERSION_STR
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QDesktopServices
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
                             QListWidgetItem,
                             QScrollArea,
                             QTabWidget,
                             QVBoxLayout, 
                             QHBoxLayout,
                             QMessageBox,
                             QInputDialog,
                             QFontDialog,
                             QColorDialog,
                             QSplashScreen,
                             QPushButton)
from Picture import Picture

developer = "paul-zz"
version = "0.01b"
py_ver = sys.version
qt_ver = QT_VERSION_STR
pyqt_ver = PYQT_VERSION_STR


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

    def setUpperText(self, text : str):
        self.upper_label.setText(text)

    def setLowerText(self, text : str):
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
        self.test_title = QLabel("没有图像。")
        self.tab_imageview.layout = QVBoxLayout()
        self.image_label_imageview = AspectLockedLabel()
        self.image_label_imageview.setImage(QPixmap("./resources/images/testimg.png"))
        self.button_edit_image = QPushButton("编辑字段")
        self.button_edit_image.setStatusTip("编辑图像上显示的文本。")
        self.button_edit_image.setIcon(QIcon("./resources/icons/ruler--pencil.png"))
        self.button_edit_font = QPushButton("更改字体")
        self.button_edit_font.setStatusTip("更改图像上文本的字体。")
        self.button_edit_font.setIcon(QIcon("./resources/icons/document-attribute.png"))
        self.button_edit_bg_color = QPushButton("背景颜色")
        self.button_edit_bg_color.setStatusTip("更改图像上文本的背景颜色。")
        self.button_edit_bg_color.setIcon(QIcon("./resources/icons/paint-can.png"))
        self.button_edit_fg_color = QPushButton("文本颜色")
        self.button_edit_fg_color.setStatusTip("更改图像上文本的颜色。")
        self.button_edit_fg_color.setIcon(QIcon("./resources/icons/palette--pencil.png"))
        
        self.tab_imageview.layout.addWidget(self.image_label_imageview)
        self.tab_imageview.layout.addWidget(self.test_title)
        self.tab_imageview.layout.addWidget(self.button_edit_image)
        self.tab_imageview.layout.addWidget(self.button_edit_font)
        self.tab_imageview.layout.addWidget(self.button_edit_bg_color)
        self.tab_imageview.layout.addWidget(self.button_edit_fg_color)
        self.tab_imageview.setLayout(self.tab_imageview.layout)

        # Global view tab
        self.test_title_global = QLabel("没有图像。")
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

        menu_edit = menubar.addMenu("编辑")
        action_edit_all_text = menu_edit.addAction("批量修改文本")
        action_edit_all_text.setIcon(QIcon("./resources/icons/ruler--pencil.png"))
        action_edit_all_text.triggered.connect(self.changeAllTexts)
        action_edit_all_font = menu_edit.addAction("批量修改字体")
        action_edit_all_font.setIcon(QIcon("./resources/icons/document-attribute.png"))
        action_edit_all_font.triggered.connect(self.changeAllFont)
        action_edit_all_fg = menu_edit.addAction("批量修改文本颜色")
        action_edit_all_fg.setIcon(QIcon("./resources/icons/palette--pencil.png"))
        action_edit_all_fg.triggered.connect(self.changeAllFontColor)
        action_edit_all_bg = menu_edit.addAction("批量修改背景颜色")
        action_edit_all_bg.setIcon(QIcon("./resources/icons/paint-can.png"))
        action_edit_all_bg.triggered.connect(self.changeAllBgColor)
        action_clear_all_text = menu_edit.addAction("清空全部文本")
        action_clear_all_text.setIcon(QIcon("./resources/icons/cross-script.png"))
        action_clear_all_text.triggered.connect(self.clearAllTexts)

        menu_window = menubar.addMenu("窗口")
        self.action_view_preview = menu_window.addAction("预览窗口")
        self.action_view_preview.setCheckable(True)
        self.action_view_preview.setChecked(True)
        self.action_view_preview.changed.connect(self.viewPreviewWindowChanged)

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
        self.image_list.itemSelectionChanged.connect(self.refreshCurrentImageView)
        self.image_list.itemDoubleClicked.connect(self.onChangeTextButtonClick)

        # Right side : preview window
        self.preview_widget = ReviewWidget()
        self.preview_window = QDockWidget("预览窗口", self)
        self.preview_window.setWidget(self.preview_widget)
        self.preview_window.visibilityChanged.connect(self.previewWindowVisChanged)
        self.preview_widget.button_edit_image.clicked.connect(self.onChangeTextButtonClick)
        self.preview_widget.button_edit_font.clicked.connect(self.onSetFontButtonClick)
        self.preview_widget.button_edit_bg_color.clicked.connect(self.onChangeBgColorButtonClick)
        self.preview_widget.button_edit_fg_color.clicked.connect(self.onChangeFgColorButtonClick)

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
                pic_data.set_name_font(QFont("msyh", 24))
                default_name = pic_data.pic_name
                new_image = ImgListItem(QPixmap(filename), filename, default_name)
                self.image_list.addImageItem(new_image, pic_data)

    def onDelImageButtonClick(self):
        # Delete the current image in the image list
        current_item = self.image_list.currentItem()
        self.image_list.takeItem(self.image_list.row(current_item))

    def refreshCurrentImageView(self):
        self.refreshImageView(self.image_list.currentItem())

    def refreshImageView(self, item : QListWidgetItem):
        # Refresh the preview window when image clicked
        if item != None:
            current_picture = item.data(Qt.UserRole)
            preview_image = current_picture.get_Qt_preview_image()
            picture_name = current_picture.pic_name
            self.preview_widget.image_label_imageview.setImage(preview_image)
            self.preview_widget.test_title.setText(picture_name)
        else:
            self.preview_widget.image_label_imageview.setImage(QPixmap("./resources/images/testimg.png"))
            self.preview_widget.test_title.setText("没有图像。")

    def refreshImageItemName(self, item : QListWidgetItem):
        # Refresh the preview window when image clicked
        if item != None:
            current_picture = item.data(Qt.UserRole)
            current_name = current_picture.pic_name
            current_widget = self.image_list.itemWidget(item)
            current_widget.setLowerText(current_name)
        else:
            self.preview_widget.image_label_imageview.setImage(QPixmap("./resources/images/testimg.png"))
            self.preview_widget.test_title.setText("没有图像。")

    def viewPreviewWindowChanged(self):
        vis = self.action_view_preview.isChecked()
        self.preview_window.setVisible(vis)

    def previewWindowVisChanged(self):
        vis = self.preview_window.isVisible()
        self.action_view_preview.setChecked(vis)

    def onGotoGithubClick(self):
        # Go to the github repository
        QDesktopServices.openUrl(QUrl("https://github.com/paul-zz/WechatLongPic/"))

    def onAboutActionClick(self):
        # Show the about dialogue
        about_dlg = QMessageBox()
        about_dlg.setWindowIcon(QIcon("./resources/icons/information-frame.png"))
        about_dlg.setWindowTitle("关于")
        about_dlg.setText(f"微信朋友圈指定缩略图长图生成器\n\n开发者: {developer} \n版本: {version} \n项目基于PyQt5开发。\nPython版本: {py_ver}\nQt版本: {qt_ver}\nPyQt版本: {pyqt_ver}")
        about_dlg.setIcon(QMessageBox.Information)
        about_dlg.exec()

    def onChangeTextButtonClick(self):
        # Event when the editing text button is clicked
        current_item = self.image_list.currentItem()
        if current_item != None:
            current_picture = current_item.data(Qt.UserRole)
            current_text = current_picture.pic_name
            text, ok = QInputDialog.getText(self, "编辑字段", "图片上的文本：", text=current_text)
            if ok:
                # Set text and refresh the review window
                current_picture.set_pic_name(text)
                self.refreshImageView(current_item)
                self.refreshImageItemName(current_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "没有选中图像！", parent=self)
            msg_box.exec()

    def onSetFontButtonClick(self):
        current_item = self.image_list.currentItem()
        if current_item != None:
            current_picture = current_item.data(Qt.UserRole)
            current_font = current_picture.name_font
            font, ok = QFontDialog.getFont(current_font, self, "选择字体")
            if ok:
                # Set text and refresh the review window
                current_picture.set_name_font(font)
                self.refreshImageView(current_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "没有选中图像！", parent=self)
            msg_box.exec()

    def onChangeBgColorButtonClick(self):
        current_item = self.image_list.currentItem()
        if current_item != None:
            current_picture = current_item.data(Qt.UserRole)
            current_color = current_picture.name_bg_color
            color = QColorDialog.getColor(current_color, self, "选择背景颜色")
            if QColor.isValid(color):
                current_picture.set_name_bg_color(color)
                self.refreshImageView(current_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "没有选中图像！", parent=self)
            msg_box.exec()

    def onChangeFgColorButtonClick(self):
        current_item = self.image_list.currentItem()
        if current_item != None:
            current_picture = current_item.data(Qt.UserRole)
            current_color = current_picture.name_color
            color = QColorDialog.getColor(current_color, self, "选择背景颜色")
            if QColor.isValid(color):
                current_picture.set_name_color(color)
                self.refreshImageView(current_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "没有选中图像！", parent=self)
            msg_box.exec()

    def changeAllTexts(self):
        image_items = [self.image_list.item(x) for x in range(self.image_list.count())]
        item_counts = len(image_items)
        if item_counts != 0:
            all_texts = [item.data(Qt.UserRole).pic_name for item in image_items]
            text_concat = "\n".join(all_texts)
            texts, ok = QInputDialog.getMultiLineText(self, "批量修改文本", "输入修改后的文本，以回车分割", text_concat)
            if ok:
                text_list = texts.split("\n")
                abandon = False
                while len(text_list) != item_counts:
                    msg_box = QMessageBox(QMessageBox.Warning, "警告", "文本行数与图像数不一致。")
                    msg_box.exec()
                    texts, ok = QInputDialog.getMultiLineText(self, "批量修改文本", "输入修改后的文本，以回车分割", texts)
                    if ok:
                        text_list = texts.split("\n")
                    else:
                        abandon = True
                        break
                if not abandon:
                    for i in range(item_counts):
                        image_item = image_items[i]
                        picture = image_item.data(Qt.UserRole)
                        picture.set_pic_name(text_list[i])
                        self.refreshImageView(image_item)
                        self.refreshImageItemName(image_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "列表中没有图像！", parent=self)
            msg_box.exec()

    def clearAllTexts(self):
        image_items = [self.image_list.item(x) for x in range(self.image_list.count())]
        item_counts = len(image_items)
        if item_counts != 0:
            msg_box = QMessageBox(QMessageBox.Warning, "注意", "确定要清除全部文本吗？", QMessageBox.Yes | QMessageBox.No, self)
            msg_box.exec()
            if msg_box.standardButton(msg_box.clickedButton()) == QMessageBox.Yes:
                for i in range(item_counts):
                    image_item = image_items[i]
                    picture = image_item.data(Qt.UserRole)
                    picture.set_pic_name("")
                    self.refreshImageView(image_item)
                    self.refreshImageItemName(image_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "列表中没有图像！", parent=self)
            msg_box.exec()

    def changeAllFontColor(self):
        image_items = [self.image_list.item(x) for x in range(self.image_list.count())]
        if len(image_items) != 0:
            color = QColorDialog.getColor(QColor(), self, "选择背景颜色")
            if QColor.isValid(color):
                for image_item in image_items:
                    picture = image_item.data(Qt.UserRole)
                    picture.set_name_color(color)
                    self.refreshImageView(image_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "列表中没有图像！", parent=self)
            msg_box.exec()

    def changeAllBgColor(self):
        image_items = [self.image_list.item(x) for x in range(self.image_list.count())]
        if len(image_items) != 0:
            color = QColorDialog.getColor(QColor(), self, "选择背景颜色")
            if QColor.isValid(color):
                for image_item in image_items:
                    picture = image_item.data(Qt.UserRole)
                    picture.set_name_bg_color(color)
                    self.refreshImageView(image_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "列表中没有图像！", parent=self)
            msg_box.exec()

    def changeAllFont(self):
        image_items = [self.image_list.item(x) for x in range(self.image_list.count())]
        if len(image_items) != 0:
            font, ok = QFontDialog.getFont(QFont(), self, "选择字体")
            if ok:
                for image_item in image_items:
                    picture = image_item.data(Qt.UserRole)
                    picture.set_name_font(font)
                    self.refreshImageView(image_item)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "列表中没有图像！", parent=self)
            msg_box.exec()


        
# Start the app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # load a splash screen
    splash_pixmap = QPixmap("./resources/images/splash.png")
    splash = QSplashScreen(splash_pixmap)
    splash.show()

    # load the main window
    window = MainWindow()
    window.show()

    # destroy the splash screen
    splash.destroy()

    # execution
    app.exec()