from PIL import Image
from Picture import Picture

class MiddlePicture(Picture):
    # A middle picture is consisted of a background picture
    # a caption and a subtitle 
    def __init__(self, size : int):
        super().__init__()
        self.caption_text = None
        self.subtitle_text = None
        self.background_alpha = 0.25
        self.background_color = "white"
        self.size = size
        

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
        print((self.width//2-self.size//2, self.height//2-self.size//2, self.width//2+self.size//2, self.height//2-self.size//2))
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
        rendered_img = Image.new("RGB", (self.size, self.size), self.background_color)
        rendered_img = Image.blend(rendered_img, self.pil_image, self.background_alpha)
        rendered_img.show()

if __name__ == "__main__":
    # Test scripts
    mid_pic = MiddlePicture(1024)
    mid_pic.load_image("D:/Code/Pics/pic6.jpg")
    mid_pic.automatic_adjust()
    mid_pic.render_image()