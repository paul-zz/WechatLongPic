from Picture import Picture
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
        pic = Picture(dir)
        pic_arranger.add_picture(pic)
    center_pic = Picture(center_dir)
    pic_arranger.set_mid_pic(center_pic)
    pic_arranger.set_output_width(1024)
    pic_arranger.generate_image()
    pic_arranger.save_output("D:/Code/Pics/output.jpg")
    
