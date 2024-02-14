import os.path
import random

import cv2
import numpy as np

all_images = ["cropped_20240103_blue_strip_1.jpg",
              "cropped_20240103_blue_strip_2.jpg",
              "cropped_20240103_capsule_1.jpg",
              "cropped_20240103_capsule_2.jpg",
              "cropped_20240103_cup.jpg",
              "cropped_20240103_frame.jpg",
              "cropped_20240103_handkerchief.jpg",
              "cropped_20240103_sharpener.jpg"]


def main():
    for i in range(7):
        path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing"
        selected_images = random.sample(all_images, 4)

        image1 = cv2.imread(os.path.join(path, selected_images[0]))
        image2 = cv2.imread(os.path.join(path, selected_images[1]))
        image3 = cv2.imread(os.path.join(path, selected_images[2]))
        image4 = cv2.imread(os.path.join(path, selected_images[3]))

        image_left = np.concatenate((image1, image2), axis=0)
        image_right = np.concatenate((image3, image4), axis=0)
        image = np.concatenate((image_left, image_right), axis=1)
        image = cv2.resize(image, (320, 240))
        # cv2.imshow("image", image)
        # cv2.waitKey(0)
        image_path = os.path.join(path, f"problem{i}.jpg")
        cv2.imwrite(image_path, image)


if __name__ == '__main__':
    main()
