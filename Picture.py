import os, io

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont, QColor

class Picture:
    # TODO: rewrite with QPixmap and QPainter
    def __init__(self):
        # The file directory to store the picture
        self.file_dir = None
        # The name of the picture, by default its filename
        self.pic_name = None
        # The pil image
        self.original_image = None # Original
        self.processed_image = None # Processed
        self.width = 0
        self.height = 0
        # Set the font
        self.name_font = QFont()
        self.name_color = QColor("white")
        self.name_bg_color = QColor("black")
        # For previewing
        self.image_preview = None
        self.changed = True
    
    def set_name_font(self, font : QFont):
        # Set the font (QFont)
        self.changed = True
        self.name_font = font

    def set_name_color(self, color : QColor):
        self.changed = True
        self.name_color = color

    def set_name_bg_color(self, color : QColor):
        self.changed = True
        self.name_bg_color = color
        
    def set_pic_name(self, name : str):
        self.changed = True
        self.pic_name = name

    def load_image(self, file_dir : str):
        self.file_dir = file_dir
        self.processed_image = QPixmap(file_dir)
        # self.processed_image = ImageOps.exif_transpose(self.processed_image)
        self.width = self.processed_image.width()
        self.height = self.processed_image.height()
        self.pic_name = file_dir.split(os.sep)[-1]
        # If the image mode is not RGB, convert it
        # if self.processed_image.mode != "RGBA":
        #     self.processed_image = self.processed_image.convert("RGBA")
        # Make a copy to the original image
        self.original_image = self.processed_image.copy()
        
    def rescale(self, new_width : int=0, new_height : int=0, fake_rescale=False):
        # Rescale the picture
        # if fake_rescale equals to True, only return the rescaled size without scaling
        self.changed = True
        if self.processed_image == None:
            raise FileNotFoundError("Image file not found or not loaded.")
        if new_width != 0 and new_height == 0:
            # Keep the original aspect ratio and calculate new_height automatically
            new_height = int(self.height/self.width*new_width)
        if new_width == 0 and new_height != 0:
            new_width = int(self.width/self.height*new_height)
        if new_width == 0 and new_height == 0:
            raise Exception("Must specify new_width or new_height or both.")
        if not fake_rescale:
            self.processed_image = self.processed_image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.width = new_width
            self.height = new_height
        return new_width, new_height

    def draw_name_on(self, image : QPixmap):
        draw = QPainter(image)
        draw.setFont(self.name_font)
        text_bound = draw.fontMetrics().boundingRect(self.pic_name)
        draw.fillRect(0, 0, text_bound.width(), text_bound.height(), self.name_bg_color)
        draw.setPen(self.name_color)
        draw.drawText(0, 0, text_bound.width(), text_bound.height(), Qt.AlignLeft, self.pic_name)
        draw.end()
        

    def draw_image_name(self):
        # Draw text
        self.draw_name_on(self.processed_image)

    def draw_image_preview(self):
        # Draw preview
        image_preview = self.original_image.copy()
        self.draw_name_on(image_preview)
        return image_preview
    
    def get_Qt_Image(self):
        return self.processed_image
    
    def get_Qt_preview_image(self):
        if self.changed:
            self.image_preview = self.draw_image_preview()
            self.changed = False
        return self.image_preview

# class PictureSH(Picture):
#     def __init__(self):
#         super().__init__()
#         # The English Name and price info
#         self.pic_name_sub = None
#         self.pic_price = None
#         # Set the font (currently the English name shares the same font with the Chinese name)
#         self.name_sub_font = ImageFont.load_default()
#         self.name_sub_color = "black"
#         self.name_sub_bg_color = "white"

#         self.price_font = ImageFont.load_default()
#         self.price_color = "white"
#         self.price_bg_color = "red"
    
#     def set_name_sub_font(self, font_name : str, font_size : int):
#         self.name_sub_font = ImageFont.truetype(font_name, font_size)

#     def set_name_sub_bg_color(self, color : str):
#         self.name_sub_bg_color = color

#     def set_name_sub_color(self, color : str):
#         self.name_sub_color = color

#     def set_price_font(self, font_name : str, font_size : int):
#         self.price_font = ImageFont.truetype(font_name, font_size)

#     def set_price_bg_color(self, color : str):
#         self.price_bg_color = color

#     def set_price_color(self, color : str):
#         self.price_color = color
        
#     def set_pic_name_sub(self, name : str):
#         self.pic_name_sub = name
    
#     def set_price(self, price : str):
#         self.pic_price = price

#     def draw_image_name(self):
#         draw = ImageDraw.Draw(self.processed_image)
#         pic_name_size = draw.textsize(self.pic_name, self.name_font)
#         pic_name_sub_size = draw.textsize(self.pic_name_sub, self.name_sub_font)
#         pic_price_size = draw.textsize(self.pic_price, self.price_font)
#         # Draw Chinese name
#         draw.rectangle((0, 0, pic_name_size[0], pic_name_size[1]), self.name_bg_color)
#         draw.text((0, 0), self.pic_name, self.name_color, font=self.name_font)
#         # Draw English name
#         draw.rectangle((0, pic_name_size[1], pic_name_sub_size[0], pic_name_size[1]+pic_name_sub_size[1]), self.name_sub_bg_color)
#         draw.text((0, pic_name_size[1]), self.pic_name_sub, self.name_sub_color, font=self.name_sub_font)
#         # Draw Price
#         draw.rectangle((self.width-pic_price_size[0], 0, self.width, pic_price_size[1]), self.price_bg_color)
#         draw.text((self.width-pic_price_size[0], 0), self.pic_price, self.price_color, font=self.price_font)