import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PicTools")

        # The label above
        self.label = QLabel("选择功能")

        # The button to enter individual functions
        self.button_start_wx = QPushButton("微信长图")
        self.button_start_custom = QPushButton("自定义拼图")

        # The layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_start_wx)
        layout.addWidget(self.button_start_custom)

        # The container
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window
        self.setCentralWidget(container)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()