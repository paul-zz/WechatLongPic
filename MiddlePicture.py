from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from Picture import Picture

class MiddlePicture(Picture):
    # A middle picture is consisted of a background picture
    # a caption and a subtitle 
    def __init__(self, size : int):
        super().__init__()
        self.caption_text = ""
        self.subtitle_text = ""
        self.background_alpha = 0.25
        self.background_color = "white"
        self.size = size
        self.caption_font = ImageFont.load_default()
        self.subtitle_font = ImageFont.load_default()
        self.caption_color = "black"
        self.subtitle_color = "black"
        self.caption_offset = 0
        
    def set_caption_font(self, font_name : str, font_size : int):
        # Set the font and font size of the caption
        self.caption_font = ImageFont.truetype(font_name, font_size)

    def set_subtitle_font(self, font_name : str, font_size : int):
        # Set the font and font size of the subtitle
        self.subtitle_font = ImageFont.truetype(font_name, font_size)

    def set_caption_text(self, text : str):
        # Set the text of the caption
        self.caption_text = text

    def set_subtitle_text(self, text : str):
        # Set the text of the subtitle
        self.subtitle_text = text
            
    def set_caption_offset(self, offset : int):
        # Set the offset of the caption
        # The caption will be moved by `offset` upwards, 
        # and the subtitle will be moved `offset` downwards
        self.caption_offset = offset

    def automatic_adjust(self):
        # This fits and crops the background picture into its size and
        if self.pil_image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        if self.width > self.height:
            # Horizontal image, fit height to size
            self.rescale(new_height=self.size)
        elif self.height >= self.width:
            # Vertical image, fit width to size
            self.rescale(new_width=self.size)
        # Crop to its center square
        self.pil_image = self.pil_image.crop((self.width//2-self.size//2, self.height//2-self.size//2, self.width//2+self.size//2, self.height//2+self.size//2))
        self.width = self.pil_image.width
        self.height = self.pil_image.height

    def set_color(self, color : str):
        self.background_color = color

    def render_image(self):
        # Render the image
        if self.pil_image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        if self.width != self.height:
            raise Exception("The background is not a square! Please adjust.")
        # Blend the image with background
        rendered_img = Image.new("RGB", (self.size, self.size), self.background_color)
        rendered_img = Image.blend(rendered_img, self.pil_image, self.background_alpha)
        # Add the caption to the image
        # Currently just add the caption to the center
        draw = ImageDraw.Draw(rendered_img)
        caption_size = draw.textsize(self.caption_text, self.caption_font)
        subtitle_size = draw.textsize(self.subtitle_text, self.subtitle_font)
        caption_x = self.size // 2 - caption_size[0] // 2
        caption_y = self.size // 2 - caption_size[1] - self.caption_offset
        subtitle_x = self.size // 2 - subtitle_size[0] // 2
        subtitle_y = self.size // 2 + self.caption_offset
        draw.text((caption_x, caption_y), self.caption_text, self.caption_color, font=self.caption_font)
        draw.text((subtitle_x, subtitle_y), self.subtitle_text, self.subtitle_color, font=self.subtitle_font)
        self.pil_image = rendered_img
        # rendered_img.show()

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