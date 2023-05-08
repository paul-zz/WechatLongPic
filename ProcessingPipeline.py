import yaml
from PictureArranger import PictureArranger
from Picture import Picture, PictureSH
from MiddlePicture import MiddlePicture

class ProcessingPipeline:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.config_dict = None

    def read_config(self):
        with open(self.config_dir, 'r', encoding="UTF-8") as file:
            config_yaml = yaml.safe_load(file)
        self.config_dict = config_yaml
    
    def process_secondhand(self):
        pic_arranger = PictureArranger()
        for index in range(0, len(self.config_dict["pictures"])):
            pic = PictureSH()
            pic.load_image(self.config_dict["pictures"][index])
            pic.set_name_font(self.config_dict["others"]["name_font"], self.config_dict["others"]["name_fontsize"])
            pic.set_name_color(self.config_dict["others"]["name_color"])
            pic.set_name_bg_color(self.config_dict["others"]["name_bg_color"])
            pic.set_name_sub_font(self.config_dict["others"]["name_sub_font"], self.config_dict["others"]["name_sub_fontsize"])
            pic.set_name_sub_color(self.config_dict["others"]["name_sub_color"])
            pic.set_name_sub_bg_color(self.config_dict["others"]["name_sub_bg_color"])
            pic.set_price_font(self.config_dict["others"]["price_font"], self.config_dict["others"]["price_fontsize"])
            pic.set_price_color(self.config_dict["others"]["price_color"])
            pic.set_price_bg_color(self.config_dict["others"]["price_bg_color"])
            pic.set_pic_name(self.config_dict["names"][index])
            pic.set_pic_name_sub(self.config_dict["names_eng"][index])
            pic.set_price(self.config_dict["prices"][index])
            pic_arranger.add_picture(pic)
        pic_arranger.set_output_width(self.config_dict["output_width"])
        pic_arranger.generate_image(type="secondhand")
        pic_arranger.save_output(self.config_dict["output"])

    def process_wechat(self):
        pic_arranger = PictureArranger()
        for index in range(0, len(self.config_dict["pictures"])):
            pic = Picture()
            pic.load_image(self.config_dict["pictures"][index])
            pic.set_name_font(self.config_dict["others"]["name_font"], self.config_dict["others"]["name_fontsize"])
            pic.set_name_color(self.config_dict["others"]["name_color"])
            pic.set_name_bg_color(self.config_dict["others"]["name_bg_color"])
            pic.set_pic_name(self.config_dict["names"][index])
            pic_arranger.add_picture(pic)
        if self.config_dict["center"]["generate_new"] == True:
            center_pic = MiddlePicture(self.config_dict["center"]["size"])
            pic_arranger.set_mid_pic(center_pic)
            center_pic.load_image(self.config_dict["center"]["background_dir"])
            center_pic.automatic_adjust()
            center_pic.set_caption_font(self.config_dict["center"]["caption_font"], self.config_dict["center"]["caption_fontsize"])
            center_pic.set_subtitle_font(self.config_dict["center"]["subtitle_font"], self.config_dict["center"]["subtitle_fontsize"])
            center_pic.set_caption_offset(self.config_dict["center"]["caption_offset"])
            center_pic.set_caption_text(self.config_dict["center"]["caption_text"])
            center_pic.set_subtitle_text(self.config_dict["center"]["subtitle_text"])
            center_pic.render_image()
        else:
            center_pic = Picture()
            center_pic.load_image(self.config_dict["center"]["background_dir"])
        pic_arranger.set_output_width(self.config_dict["output_width"])
        pic_arranger.generate_image()
        pic_arranger.save_output(self.config_dict["output"])

    def process(self):
        if self.config_dict == None:
            raise Exception("Please read config file first.")
        if "type" in self.config_dict:
            type = self.config_dict["type"]
        else:
            type = "wechat"
        
        if type == "wechat":
            self.process_wechat()
        elif type == "secondhand":
            self.process_secondhand()

