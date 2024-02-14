import os.path

import cv2

from utils import crop_image

all_images = [
    "problem1.jpg",
    "problem2.jpg",
    "problem3.jpg",
    "problem4.jpg",
    "problem5.jpg",
    "problem6.jpg",
    "problem7.jpg",
    "problem8.jpg",
    "problem9.jpg",
    "problem10.jpg",
    "problem11.jpg",
    "problem12.jpg",
    "problem13.jpg",
    "problem14.jpg",
    "problem15.jpg",
    "problem16.jpg",
    "problem17.jpg",
]


def main():
    for i, image_name in enumerate(all_images):
        path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/problems"
        image_path = os.path.join(path, image_name)

        image = cv2.imread(image_path)
        print(image.shape)


def main2():
    """
    ratio = 4: 3
    image_size = 640, 480 / 1280, 960 / 1920,  1440 / 2560, 1920

    :return:
    """
    """----------------------------------"""
    number = 17

    # is_rotate = True
    is_rotate = False
    # is_save = True
    is_save = False

    # xywh = [500, 400, 3000, 2250]
    xywh = [600, 450, 2880, 2160]
    """----------------------------------"""

    image_name = all_images[number]
    path = "/home/changmin/PycharmProjects/GPT_examples/data/bin_packing/problems"
    image_path = os.path.join(path, image_name)

    image = cv2.imread(image_path)

    # (4000, 3000, 3) // [x, y, 3000, 2250] => (640, 480)
    if is_rotate:
        image = cv2.rotate(image, cv2.ROTATE_180)
    cropped_image = crop_image(image, xywh)

    resized_image = cv2.resize(cropped_image, (640, 480))
    cv2.imshow("cropped_image", resized_image)
    cv2.waitKey(0)
    if is_save:
        cv2.imwrite(os.path.join(path, f"problem{number}.jpg"), resized_image)
        print("Save Done")


if __name__ == '__main__':
    main()
