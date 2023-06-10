import cv2
import numpy as np

class ImageModel:
    def __init__(self, file_name):
        self.file_name = file_name
        self.image = None

    def load_image(self):
        self.image = cv2.imread(self.file_name)

    def get_image(self):
        return self.image


class ImageProcessingModel:
    def __init__(self, image):
        self.image = image

    def truncate_channel(self, start_col, end_col):
        # Truncate the image channel based on start and end columns
        truncated_image = self.image[:, start_col:end_col]
        return truncated_image

    def calculate_channel_means(self, truncated_image, start_row, end_row):
        # Calculate the mean values of the color channels
        red_channel = np.mean(truncated_image[:, :, 2][start_row:end_row], axis=1)
        green_channel = np.mean(truncated_image[:, :, 1][start_row:end_row], axis=1)
        blue_channel = np.mean(truncated_image[:, :, 0][start_row:end_row], axis=1)
        return red_channel, green_channel, blue_channel

    def transform_array_proportions(self, arr, new_length):
        old_length = len(arr)
        indices = np.linspace(0, old_length - 1, num=new_length)
        new_arr = np.interp(indices, np.arange(old_length), arr)
        return new_arr
