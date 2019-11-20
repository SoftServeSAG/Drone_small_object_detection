import cv2
import json
import os
import numpy as np
import imutils

dataset_location = "./dataset/"
output_folder = "./unet/data/validation/"


def resize_image(img, size):
    h, w, c = img.shape
    new_h, new_w = size
    # mask = np.zeros((size[0], size[1], c), dtype=img.dtype)
    if h > w:
        resized = imutils.resize(img, height=new_h)
        if resized.shape[1] > new_w:
            resized = imutils.resize(img, width=new_w)

    elif w >= h:
        resized = imutils.resize(img, width=new_w)
        if resized.shape[0] > new_h:
            resized = imutils.resize(img, height=new_h)

    resized_h, resized_w = resized.shape[0], resized.shape[1]

    return cv2.copyMakeBorder(resized, (new_h - resized_h) // 2, new_h - resized_h - (new_h - resized_h) // 2,
                              (new_w - resized_w) // 2, new_w - resized_w - (new_w - resized_w) // 2,
                              cv2.BORDER_CONSTANT, value=(0, 0, 0))

files = list(filter(lambda x: x[-3:] == "jpg", os.listdir(dataset_location)))

count = 1
for img_file in files:
    json_file = img_file[:-3] + "json"
    img = cv2.imread(dataset_location + img_file)
    blank_image = np.zeros(shape=(img.shape[0], img.shape[1], 1), dtype=np.uint8)
    if os.path.isfile(dataset_location + json_file):
        with open(dataset_location + json_file, "r") as f:
            data = json.load(f)["segmentation"]
            for entry in data:
                points = list(map(lambda x: [int(round(x[0])), int(round(x[1]))],
                                  zip(entry[0::2], entry[1::2]
                                      )))
                cv2.fillPoly(blank_image, np.int32([points]), 255)

    resized_img = resize_image(img, size=(480, 640))
    if resized_img.shape[0] != 480 or resized_img.shape[1] != 640:
        raise Exception("inconsistency on img")
    resized_map = resize_image(blank_image, size=(480, 640))
    if resized_map.shape[0] != 480 or resized_map.shape[1] != 640:
        raise Exception("inconsistency on map")

    cv2.imwrite(f"{output_folder}img/{img_file}", resized_img)
    cv2.imwrite(f"{output_folder}mask/{img_file[:-3]}png", resized_map)
    print(f"[{count} / {len(files)}] - " + f"{output_folder}<type>/{img_file[:-4]}")
    count += 1
