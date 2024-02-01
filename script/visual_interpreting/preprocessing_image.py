import os.path

import cv2


def crop_image(image, xywh):
    real_h = image.shape[0]
    real_w = image.shape[1]
    x, y, w, h = xywh

    # if real_h > real_w:
    #     image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #     real_h = image.shape[0]
    #     real_w = image.shape[1]
    #     pass
    if x + w > real_w:
        print("insert value under", real_w, ", input: ", w)
        raise ValueError
    if y + h > real_h:
        print("insert value under", real_h, ", input: ", h)
        raise ValueError

    cropped_image = image[y: y + h, x: x + w, :]
    return cropped_image


def main():
    image_path = "./data/examples_240103_shape/examples_240103_shape_original"
    save_path = "./data/examples_240103_shape/examples_240103_shape_cropped"
    name = "20240103_triangle.jpg"
    image = cv2.imread(os.path.join(image_path, name))

    print(image.shape)

    image = crop_image(image, [550, 300, 3200, 2400])
    image = cv2.resize(image, (320, 240))
    cv2.imshow("cropped image", image)
    cv2.waitKey(0)
    cv2.imwrite(os.path.join(save_path, "cropped_" + name), image)


if __name__ == '__main__':
    main()
