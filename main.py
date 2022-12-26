import sys
from Picture import Picture
from MiddlePicture import MiddlePicture
from PictureArranger import PictureArranger
from ProcessingPipeline import ProcessingPipeline

if __name__ == "__main__":
    try:
        config_dir = sys.argv[1]
        pipeline = ProcessingPipeline(config_dir)
        pipeline.read_config()
        pipeline.process()
        print("The image has been processed successfully!")
    except Exception as e:
        print("Not successful: " + str(e))
    
