import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class Picture:
    def __init__(self):
        # The file directory to store the picture
        self.file_dir = None
        # The name of the picture, by default its filename
        self.pic_name = None
        # The pil image
        self.pil_image = None
        self.width = 0
        self.height = 0
        # Set the font
        self.name_font = ImageFont.load_default()
        self.name_color = "white"
    
    def set_name_font(self, font_name : str, font_size : int):
        # Set the font and font size of the name on each image
        self.name_font = ImageFont.truetype(font_name, font_size)

    def set_pic_name(self, name : str):
        self.pic_name = name

    def load_image(self, file_dir : str):
        self.file_dir = file_dir
        self.pil_image = Image.open(self.file_dir)
        self.width = self.pil_image.width
        self.height = self.pil_image.height
        self.pic_name = file_dir.split(os.sep)[-1]
        # If the image mode is not RGB, convert it
        if self.pil_image.mode != "RGB":
            self.pil_image = self.pil_image.convert("RGB")

    def rescale(self, new_width : int=0, new_height : int=0, fake_rescale=False):
        # Rescale the picture
        # if fake_rescale equals to True, only return the rescaled size without scaling
        if self.pil_image == None:
            raise FileNotFoundError("Image file not found or not loaded.")
        if new_width != 0 and new_height == 0:
            # Keep the original aspect ratio and calculate new_height automatically
            new_height = int(self.height/self.width*new_width)
        if new_width == 0 and new_height != 0:
            new_width = int(self.width/self.height*new_height)
        if new_width == 0 and new_height == 0:
            raise Exception("Must specify new_width or new_height or both.")
        if not fake_rescale:
            self.pil_image = self.pil_image.resize((new_width, new_height))
            self.width = new_width
            self.height = new_height
        return new_width, new_height

    def draw_image_name(self):
        draw = ImageDraw.Draw(self.pil_image)
        pic_name_size = draw.textsize(self.pic_name, self.name_font)
        # TODO: Add option for the position of name text
        draw.rectangle((0, 0, pic_name_size[0], pic_name_size[1]), "black")
        draw.text((0, 0), self.pic_name, self.name_color, font=self.name_font)

    def show_image(self):
        # Show the image in PIL window, for debugging
        self.pil_image.show()