import cv2
import numpy as np

image_1 = "./data/object_shape_examples/1d_shape.png"
image_2 = "./data/object_shape_examples/1d_shape_circle.jpg"

image1 = cv2.imread(image_1)
image2 = cv2.imread(image_2)

image1 = cv2.resize(image1, (320, 240))
image2 = cv2.resize(image2, (320, 240))
image = np.concatenate((image1, image2), axis=0)

cv2.imshow("test", image)
cv2.waitKey(0)
cv2.imwrite("../../data/object_shape_examples/1d_shape.jpg", image)
# print()
