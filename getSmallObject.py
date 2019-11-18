import os
import json
import sys
import math
import cv2

dataJson = "data.json"
resultJson = "resultFromModel.json"

path_to_images = "camp/"

with open(dataJson) as json_file:
    data = json.load(json_file)
    for key in data:
        bboxes = data[key]
        for bbox in bboxes:
            height = math.sqrt(((bbox[0] - bbox[0]) ** 2) + ((bbox[1] - bbox[3]) ** 2))
            width = math.sqrt(((bbox[0] - bbox[2]) ** 2) + ((bbox[1] - bbox[1]) ** 2))
            area = height*width
            img = cv2.imread(path_to_images + key)
            img_area =img.shape[0] * img.shape[1]
            persent = (area*100)/img_area
            print(persent)
            sys.exit()