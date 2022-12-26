from Picture import Picture
from MiddlePicture import MiddlePicture
from PictureArranger import PictureArranger

if __name__ == "__main__":
    pic_dirs = ["D:/Code/Pics/pic1.jpg",
    "D:/Code/Pics/pic4.png",
    "D:/Code/Pics/pic2.jpg",
    "D:/Code/Pics/pic3.jpeg",
    "D:/Code/Pics/pic5.jpg",
    "D:/Code/Pics/pic6.jpg"
    ]
    center_dir = "D:/Code/Pics/center.png"
    pic_arranger = PictureArranger()
    for dir in pic_dirs:
        pic = Picture()
        pic.load_image(dir)
        pic.set_name_font("msyh", 20)
        pic.set_pic_name("AFOIE-呵呵呵")
        pic_arranger.add_picture(pic)
    # center_pic = Picture()
    # center_pic.load_image(center_dir)
    center_pic = MiddlePicture(1024)
    pic_arranger.set_mid_pic(center_pic)
    center_pic.load_image("D:/Code/Pics/pic2.jpg")
    center_pic.automatic_adjust()
    center_pic.set_caption_font("msyhbd", 150)
    center_pic.set_subtitle_font("msyh", 50)
    center_pic.set_caption_offset(25)
    center_pic.set_caption_text("标题测试")
    center_pic.set_subtitle_text("这个是小标题")
    center_pic.render_image()
    pic_arranger.set_output_width(1024)
    pic_arranger.generate_image()
    pic_arranger.save_output("D:/Code/Pics/output.jpg")
    
