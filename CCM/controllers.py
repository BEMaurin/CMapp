import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt
import pandas as pd
from models import *

class ImageController:
    def __init__(self, image_model, image_processing_model):
        self.image_model = image_model
        self.image_processing_model = image_processing_model
        self.mouse_loc = []
        self.rf = pd.DataFrame(columns=["rf", "produit"])
        self.fig, self.ax = plt.subplots()

    def select_images(self):
        Tk().withdraw()
        file_names = askopenfilenames(
            title="Sélectionnez des photos",
            filetypes=(("Fichiers image", "*.jpg;*.jpeg;*.png"), ("Tous les fichiers", "*.*"))
        )
        for file_name in file_names:
            if file_name:
                self.image_model = ImageModel(file_name)
                self.image_model.load_image()

                self.display_image()

                self.setup_mouse_callback()

                while True:
                    # Handle mouse events and key presses
                    if cv2.waitKey(1) & 0xFF == ord('\r'):
                        break
                    if cv2.waitKey(1) & 0xFF == 27:
                        exit()

                cv2.destroyAllWindows()
                self.process_image()
            else:
                print('Aucune image sélectionnée.')

    def display_image(self):
        
        resized_image = cv2.resize(self.image_model.get_image(), (0, 0), fx=1 / 3, fy=1 / 3)
        cv2.imshow('Image', resized_image)

    def setup_mouse_callback(self):
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.handle_mouse_click(x, y)

        cv2.setMouseCallback('Image', mouse_callback)

    def handle_mouse_click(self, x, y):
        if len(self.mouse_loc) < 2:
            self.mouse_loc.append(y * 3)
            print(self.mouse_loc)
        else:
            self.mouse_loc.append(x * 3)
            print(self.mouse_loc)

    def process_image(self):
        truncated_image = self.image_processing_model.truncate_channel(self.mouse_loc[2] - 10,
                                                                       self.mouse_loc[2] + 10)

        red_channel, green_channel, blue_channel = self.image_processing_model.calculate_channel_means(
            truncated_image, self.mouse_loc[0], self.mouse_loc[1])

        red_channel = self.image_processing_model.transform_array_proportions(red_channel[::-1], 1000)
        green_channel = self.image_processing_model.transform_array_proportions(green_channel[::-1], 1000)
        blue_channel = self.image_processing_model.transform_array_proportions(blue_channel[::-1], 1000)

        # Further processing and plotting can be added here

    def handle_plot_click(self, event):
        if event.button == 1:  # Left mouse button
            self.rf = pd.concat([self.rf, pd.DataFrame([[np.round(event.xdata / 1000, 2), ""]],
                                                       columns=["rf", "produit"])], join="inner")
            self.rf.to_clipboard(index=False)

        # Additional event handling code can be added here
