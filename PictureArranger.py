from PIL import Image
from Picture import Picture

class PictureArranger:
    def __init__(self):
        self.picture_array = []
        self.output_width = 0
        self.mid_pic = None
        self.output_img = None
        self.filling_color = "white"

    def add_picture(self, pic: Picture):
        self.picture_array.append(pic)

    def set_mid_pic(self, pic:Picture):
        self.mid_pic = pic

    def set_filling_color(self, color : str):
        self.filling_color = color

    def set_output_width(self, output_width: int):
        self.output_width = output_width

    def get_nearest_index(self, lst: list, value: int):
        min_idx = -1
        min_dist = lst[0]-value
        for index in range(0, len(lst)):
            dist = lst[index]-value
            if abs(dist) < abs(min_dist):
                min_dist = dist
                min_idx = index
        return min_idx, min_dist


    def generate_image(self):
        # Generate output picture
        if self.output_width == 0:
            raise Exception("Please specify the width of output picture.")
        if self.mid_pic == None:
            raise Exception("Please select the middle picture!")
        # Calculating overall height
        # Height is currently not including the middle picture
        height = 0
        # The array to store the Y coordinate of the top of each picture
        # Starting from zero
        pos_array = []
        for pic in self.picture_array:
            pos_array.append(height)
            _, pic_rescaled_height = pic.rescale(new_width=self.output_width, fake_rescale=True)
            height += pic_rescaled_height
        # Where the middle picture should be placed
        _, mid_pic_height = self.mid_pic.rescale(new_height=self.output_width)
        pos_mid = height // 2 
        # Insert the middle picture to the nearest position to the center
        # and calculate the distance to the center
        idx_near, center_dist = self.get_nearest_index(pos_array, pos_mid)
        pos_near = pos_array[idx_near]
        pos_array.insert(idx_near, pos_near)
        for index in range(idx_near+1, len(pos_array)):
            pos_array[index] += mid_pic_height
        # Adjust other pictures to ensure the middle picture is centered and output
        # Create a blank image on which paste all the pictures
        output_img = Image.new("RGB", (self.output_width, height + mid_pic_height + 2*abs(center_dist)), self.filling_color)
        # If the middle picture is too high, move all pictures to below
        if center_dist < 0:
            for index in range(0, len(pos_array)):
                pos_array[index] += 2*abs(center_dist)
        # Else, just paste the pictures one by one from the top to the blank new image
        pics_to_paste = self.picture_array.copy()
        pics_to_paste.insert(idx_near, self.mid_pic)
        for index in range(0, len(pics_to_paste)):
            pic_to_paste = pics_to_paste[index]
            pic_to_paste.rescale(new_width=self.output_width)
            if index != idx_near:
                # If the picture is not the center picture, draw its name
                pic_to_paste.draw_image_name()        
            output_img.paste(pic_to_paste.pil_image, (0, pos_array[index]))
        self.output_img = output_img

    def save_output(self, save_dir):
        self.output_img.save(save_dir)
    

        
    