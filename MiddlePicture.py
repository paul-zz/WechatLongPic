from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
from Picture import Picture

# TODO: Rewrite using Qt
class MiddlePicture(Picture):
    # A middle picture is consisted of a background picture
    # a caption and a subtitle 
    def __init__(self, size : int):
        super().__init__()
        self.caption_text = ""
        self.subtitle_text = ""
        self.background_alpha = 0.25
        self.background_color = QColor("white")
        self.size = size
        self.caption_font = QFont()
        self.subtitle_font = QFont()
        self.caption_color = QColor("black")
        self.subtitle_color = QColor("black")
        self.caption_offset = 0
    
    def set_size(self, size : int):
        self.size = size
        
    def set_background_alpha(self, alpha : float):
        self.background_alpha = alpha
        self.changed = True
        
    def set_background_color(self, color : QColor):
        self.background_color = color
        self.changed = True

    def set_caption_font(self, font : QFont):
        # Set the font and font size of the caption
        self.caption_font = font
        self.changed = True

    def set_subtitle_font(self, font : QFont):
        # Set the font and font size of the subtitle
        self.subtitle_font = font
        self.changed = True

    def set_caption_text(self, text : str):
        # Set the text of the caption
        self.caption_text = text
        self.changed = True
    
    def set_caption_color(self, color : QColor):
        # Set the color of the caption
        self.caption_color = color
        self.changed = True
    
    def set_subtitle_color(self, color : QColor):
        # Set the color of the subtitle
        self.subtitle_color = color
        self.changed = True

    def set_subtitle_text(self, text : str):
        # Set the text of the subtitle
        self.subtitle_text = text
        self.changed = True
            
    def set_caption_offset(self, offset : int):
        # Set the offset of the caption
        # The caption will be moved by `offset` upwards, 
        # and the subtitle will be moved `offset` downwards
        self.caption_offset = offset
        self.changed = True

    def automatic_adjust_on(self, image : QPixmap):
        # This fits and crops the background picture into its size and
        if image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        if image.width() > image.height():
            # Horizontal image, fit height to size
            image = image.scaledToHeight(self.size, Qt.SmoothTransformation)
        elif image.height() >= image.width():
            # Vertical image, fit width to size
            image = image.scaledToWidth(self.size, Qt.SmoothTransformation)
        # Crop to its center square
        image = self.crop(image, QRect(image.width()//2-self.size//2, image.height()//2-self.size//2, self.size, self.size))
        return image

    def automatic_adjust(self):
        self.processed_image = self.automatic_adjust_on(self.processed_image)
        self.width = self.processed_image.width
        self.height = self.processed_image.height
        self.changed = True

    def set_color(self, color : str):
        self.background_color = color
        self.changed = True

    def render_image_on(self, image : QPixmap):
        # Render the image
        if image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        if image.width() != image.height():
            print(f"Image width {image.width()} but image height {image.height()}")
            raise Exception("The background is not a square! Please adjust.")
        
        rendered_img = QPixmap(self.size, self.size)
        rendered_img.fill(self.background_color)
        draw = QPainter(rendered_img)
        # Blend the image with background
        draw.setOpacity(self.background_alpha)
        draw.drawPixmap(0, 0, image)
        # Add the caption to the image
        # Currently just add the caption to the center
        draw.setFont(self.caption_font)
        draw.setOpacity(1.0)
        caption_bound = draw.fontMetrics().boundingRect(self.caption_text)
        caption_x = self.size // 2 - caption_bound.width() // 2
        caption_y = self.size // 2 - caption_bound.height() - self.caption_offset
        draw.setPen(self.caption_color)
        draw.drawText(caption_x, caption_y, caption_bound.width(), caption_bound.height(), Qt.AlignLeft, self.caption_text)

        draw.setFont(self.subtitle_font)
        subtitle_bound = draw.fontMetrics().boundingRect(self.subtitle_text)
        subtitle_x = self.size // 2 - subtitle_bound.width() // 2
        subtitle_y = self.size // 2 + self.caption_offset
        draw.setPen(self.subtitle_color)
        draw.drawText(subtitle_x, subtitle_y, subtitle_bound.width(), subtitle_bound.height(), Qt.AlignLeft, self.subtitle_text)

        draw.end()
        return rendered_img
    
    def render_image(self):
        self.processed_image = self.automatic_adjust_on(self.original_image)
        self.processed_image = self.render_image_on(self.processed_image)
        self.changed = True

    def draw_image_preview(self):
        # Draw preview - overridden
        image_preview = self.original_image.copy()
        image_preview = self.automatic_adjust_on(image_preview)
        image_preview = self.render_image_on(image_preview)
        return image_preview

if __name__ == "__main__":
    # Test scripts
    mid_pic = MiddlePicture(1024)
    mid_pic.load_image("D:/Code/Pics/pic2.jpg")
    mid_pic.automatic_adjust()
    mid_pic.set_caption_font("msyhbd", 150)
    mid_pic.set_subtitle_font("msyh", 50)
    mid_pic.set_caption_offset(25)
    mid_pic.set_caption_text("标题测试")
    mid_pic.set_subtitle_text("这个是小标题")
    mid_pic.render_image()