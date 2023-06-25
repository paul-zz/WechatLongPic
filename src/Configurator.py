from PyQt5.QtGui import QColor
class Configurator:
    def __init__(self):
        self.use_midpic = False
        self.midpic = None
        self.output_width = 1024
        self.bg_color = QColor("white")