from models import ImageModel, ImageProcessingModel
from controllers import ImageController

# Factor of image reduction
reduction = 3
width = 10

def main():
    image_model = ImageModel('')
    image_processing_model = ImageProcessingModel(None)
    image_controller = ImageController(image_model, image_processing_model)
    image_controller.select_images()


if __name__ == '__main__':
    main()
