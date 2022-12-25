from PIL import Image
from Picture import Picture

class MiddlePicture(Picture):
    # A middle picture is consisted of a background picture
    # a caption and a subtitle 
    def __init__(self, size : int):
        super().__init__()
        self.caption_text = None
        self.subtitle_text = None
        self.background_alpha = 25
        self.size = size

    def automatic_adjust(self):
        # This fits and crops the background picture into its size and
        if self.pil_image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        

    def render_image(self):
        # Render the image
        if self.pil_image == None:
            raise FileExistsError("Background image file not found or not loaded.")
        if self.width != self.height:
            raise Exception("The background is not a square! Please adjust.")
        rendered_img = Image.new("RGB", )