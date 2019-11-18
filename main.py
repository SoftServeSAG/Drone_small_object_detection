import argparse
import os
import glob
import cv2
import numpy as np
import sys
import csv
import json
import numpy as np
from pycocotools import mask
from skimage import measure
from pycocotools import coco
import urllib.request

def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return [int(min(x_coordinates)), int(min(y_coordinates)), int(max(x_coordinates)), int(max(y_coordinates))]

def new_mask_annotation(path_to_mask):
    path_to_masks = glob.glob(os.path.join(path_to_mask, '*.png'))
    for index in range(len(path_to_masks)):
        print(index)
        image_name = path_to_masks[index].split('/')[1].split('.')[0]
        img_mask = cv2.imread(path_to_masks[index], cv2.IMREAD_GRAYSCALE)
        ground_truth_binary_mask = np.array(img_mask)
        fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask)
        encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
        ground_truth_area = mask.area(encoded_ground_truth)
        ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
        contours = measure.find_contours(ground_truth_binary_mask, 0.5)

        bboxes = []
        for contour in contours:
            bbox = bounding_box(contour)
            bboxes.append(bbox)

        annotation = {
            "segmentation": [],
            "area": ground_truth_area.tolist(),
            "iscrowd": 0,
            "image_id": image_name,
            "bbox": bboxes,
            "category_id": 1,
            "id": index
        }

        for contour in contours:
            contour = np.flip(contour, axis=1)
            segmentation = contour.ravel().tolist()
            annotation['segmentation'].append(segmentation)

            with open('RosbagJson/{}.json'.format(image_name), 'w') as my_file:
                json.dump(annotation, my_file)

if __name__ == '__main__':
    with open('rosbag2.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in readCSV:
            index += 1
            if index < 0:
                continue
            data = row[3]
            if len(data) < 40:
                continue
            data = json.loads(data)
            link = data["objects"][0]["instanceURI"]
            print(link)
            mask_name = row[9].split('.')[0]
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(link, "RosbagMask2/{}.png".format(mask_name))
            print(index)
            
    new_mask_annotation("RosbagMask2/")

